import pandas as pd
import numpy as np
import math
import time
import json
from typing import Iterable, List, Tuple
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

# Dataset of ALL census tracts and some incorrectly named variables, used to compile on
df = pd.read_csv('Census_Reporter_API_calls/acs_tracts_2023_ioc_features.csv')
# print(df.head())

# print(df.columns) # cols in current df

df = df[['geoid', 'state_fips', 'county_fips', 'tract_code', 'NAME','pop_1plus']] # Keep only the useful columns (some names are wrong)
# print(df.head())


'''
---------------------------------------------------------------------------------------------------------------------
Functions to call Census reporter API for variables based on census tracts, 
- now can call multiple tracts at a time, and calls are parrelelized :)
---------------------------------------------------------------------------------------------------------------------
'''

CR_BASE = "https://api.censusreporter.org/1.0/data/show"

def _normalize_geoid(g):
    """
    Accepts either full GEOID like '14000US49005001100' or bare 11-digit '49005001100'.
    Returns the full Census Reporter tract GEOID.
    """
    s = str(g)
    if s.startswith("14000US"):
        return s
    # 11-digit tract id (state2 + county3 + tract6)
    if len(s) == 11 and s.isdigit():
        return "14000US" + s
    # If it's something else (e.g., already prefixed but malformed), just pass through.
    return s

def _chunked(seq: Iterable[str], n: int) -> List[List[str]]:
    """Chunk an iterable into lists of size n."""
    chunk = []
    for item in seq:
        chunk.append(item)
        if len(chunk) == n:
            yield chunk
            chunk = []
    if chunk:
        yield chunk

def fetch_cr_variable_for_tracts(
    df: pd.DataFrame,
    geoid_col: str,
    table_id: str,
    col_id: str,
    acs: str = "latest",
    batch_size: int = 45,
    max_workers: int = 8,
    request_timeout: float = 15.0,
) -> pd.DataFrame:


    def _normalize_geoid(g):
        s = str(g)
        if s.startswith("14000US"):
            return s
        if len(s) == 11 and s.isdigit():
            return "14000US" + s
        return s

    def _chunked(seq, n):
        chunk = []
        for item in seq:
            chunk.append(item)
            if len(chunk) == n:
                yield chunk
                chunk = []
        if chunk:
            yield chunk

    def _fetch_batch(session, geoids, table_id, col_id, acs, timeout=15.0, max_retries=3, backoff=0.8):
        url = f"https://api.censusreporter.org/1.0/data/show/{acs}"
        params = {"table_ids": table_id, "geo_ids": ",".join(geoids)}
        last_exc = None
        for attempt in range(max_retries):
            try:
                r = session.get(url, params=params, timeout=timeout)
                if r.status_code in (429, 500, 502, 503, 504):
                    raise requests.HTTPError(f"HTTP {r.status_code}", response=r)
                r.raise_for_status()
                j = r.json()
                out = []
                data = j.get("data", {})
                for geoid in geoids:
                    rec = data.get(geoid, {}).get(table_id, {})
                    est = rec.get("estimate", {}).get(col_id, None)
                    moe = rec.get("error", {}).get(col_id, None)
                    out.append((geoid, est, moe))
                return out
            except (requests.Timeout, requests.ConnectionError, requests.HTTPError, json.JSONDecodeError):
                # simple exponential backoff with slight growth
                time.sleep((backoff ** attempt) * (1.0 + 0.25 * attempt))
        return [(g, None, None) for g in geoids]

    all_geoids = df[geoid_col].astype(str).map(_normalize_geoid)
    unique_geoids = list(pd.unique(all_geoids))
    batches = list(_chunked(unique_geoids, batch_size))

    results = []
    with requests.Session() as session:
        session.headers.update({"User-Agent": "cr-batcher/1.0"})
        with ThreadPoolExecutor(max_workers=max_workers) as pool:
            futs = [pool.submit(_fetch_batch, session, b, table_id, col_id, acs, request_timeout) for b in batches]
            for fut in as_completed(futs):
                results.extend(fut.result())

    # Build result DF and rename the right-side 'geoid' to the temp key
    res_df = pd.DataFrame(results, columns=["__geoid_norm", "estimate", "moe"])

    # Merge on the normalized values, keeping your original geoid column name intact
    out = (
        df.assign(__geoid_norm=all_geoids.values)
          .merge(res_df, on="__geoid_norm", how="left")
          .drop(columns="__geoid_norm")
    )
    return out


def fetch_multiple_no_moe(df, geoid_col, vars_dict):
    """
    Fetch multiple ACS variables from Census Reporter (estimates only).
    vars_list: list of (table_id, col_id)
    Returns df with one estimate column per variable.
    """
    from functools import reduce

    results = []
    vars_list  = [vars_dict[key] for key in vars_dict.keys()] # extract features from var's dictionary
    for table_id, col_id in vars_list:
        out = fetch_cr_variable_for_tracts(
            df=df,
            geoid_col=geoid_col,
            table_id=table_id,
            col_id=col_id,
            acs="latest",
            batch_size=45,
            max_workers=8
        )

        # Keep only GEOID + estimate; rename it cleanly
        var_name = f"{table_id}_{col_id[-3:]}"  # e.g., B01003_001
        out = out[[geoid_col, "estimate"]].rename(columns={"estimate": var_name})
        results.append(out)

    merged = reduce(lambda left, right: left.merge(right, on=geoid_col, how="left"), results)
    return merged

def rename_cols(df, vars_dict):
    """
    vars_dict like:
      {"total population": ("B01003", "B01003001"),
       "median household income": ("B19013", "B19013001")}
    """
    df = df.copy()
    df.columns = df.columns.map(str)   # normalize to strings

    # reverse map: col_id -> friendly
    rev = {v[1]: k for k, v in vars_dict.items()}

    norm = lambda c: str(c).upper().replace("_", "")  # turn 'b01003_001' -> 'B01003001'

    to_rename = {c: rev[norm(c)] for c in df.columns if norm(c) in rev}
    return df.rename(columns=to_rename)



'''
------------------------------------------------------------------------------------------------------------------------
WORKING AREA
------------------------------------------------------------------------------------------------------------------------
'''


Raw_Variables_Dictionary = {
    # 'Variable name' : ('Table_ID', 'Variable_ID')
    'total population' : ("B01003", "B01003001"),
    'median household income' : ("B19013", "B19013001"),
    'median age' : ("B01002", "B01002001"),
    'Means of transportation to work: Public transportation' : ('B08301', 'B08301010'),
    'Travel Time to Work Total' : ('B08303', 'B08303001'),
    # Time to work by Public Transit
    "Total Travel Time to Work via Public transportation" : ('B08134', 'B08134061'),
    "Less than 10 minutes Travel Time to Work via Public transportation" : ('B08134','B08134062'),
    "10 to 14 minutes Travel Time to Work via Public transportation" : ('B08134','B08134063'),
    "15 to 19 minutes Travel Time to Work via Public transportation" : ('B08134','B08134064'),
    "20 to 24 minutes Travel Time to Work via Public transportation" : ('B08134','B08134065'),
    "25 to 29 minutes Travel Time to Work via Public transportation" : ('B08134','B08134066'),
    "30 to 34 minutes Travel Time to Work via Public transportation" : ('B08134','B08134067'),
    "35 to 44 minutes Travel Time to Work via Public transportation" : ('B08134','B08134068'),
    "45 to 59 minutes Travel Time to Work via Public transportation" : ('B08134','B08134069'),
    "60 or more minutes Travel Time to Work via Public transportation" : ('B08134','B08134070'),

    # Time to work by Driving (with no carpooling)
    "Total Travel Time to Work via Driving Alone" : ('B08134','B08134021'),
    "Less than 10 minutes Travel Time to Work via Driving Alone" : ('B08134','B08134022'),
    "10 to 14 minutes Travel Time to Work via Driving Alone" : ('B08134','B08134023'),
    "15 to 19 minutes Travel Time to Work via Driving Alone" : ('B08134','B08134024'),
    "20 to 24 minutes Travel Time to Work via Driving Alone" : ('B08134','B08134025'),
    "25 to 29 minutes Travel Time to Work via Driving Alone" : ('B08134','B08134026'),
    "30 to 34 minutes Travel Time to Work via Driving Alone" : ('B08134','B08134027'),
    "35 to 44 minutes Travel Time to Work via Driving Alone" : ('B08134','B08134028'),
    "45 to 59 minutes Travel Time to Work via Driving Alone" : ('B08134','B08134029'),
    "60 or more minutes Travel Time to Work via Driving Alone" : ('B08134','B08134030')
}

# Uses only first 100 rows for testing purposes. (comment out when compiling final dataset)
df=df.head(100)

# call the variables for the df
raw_vars_df = fetch_multiple_no_moe(df, "geoid", Raw_Variables_Dictionary)

raw_vars_df = rename_cols(raw_vars_df, Raw_Variables_Dictionary)

merge_df = pd.merge(df, raw_vars_df, on='geoid', how='inner')

print('heading: \n', merge_df.head())

print(merge_df.columns)

print(merge_df[['Total Travel Time to Work via Driving Alone',
                'Total Travel Time to Work via Public transportation','Travel Time to Work Total']].head())

merge_df.to_csv('/workspaces/Urban-Ant/Census_Reporter_API_calls/RawData.csv', index = False)
