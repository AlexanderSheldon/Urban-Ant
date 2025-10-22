import pandas as pd
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
    import pandas as pd
    from concurrent.futures import ThreadPoolExecutor, as_completed
    import requests

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
        import time, json, requests
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


def fetch_multiple_no_moe(df, geoid_col, vars_list):
    """
    Fetch multiple ACS variables from Census Reporter (estimates only).
    vars_list: list of (table_id, col_id)
    Returns df with one estimate column per variable.
    """
    from functools import reduce

    results = []
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

'''
------------------------------------------------------------------------------------------------------------------------
WORKING AREA
------------------------------------------------------------------------------------------------------------------------
'''


variables = [
    # ("Table_ID", "Variable_ID"), Table Name, Variable Name
    ("B01003", "B01003001"),  # total population
    ("B19013", "B19013001"),  # median household income
    ("B01002", "B01002001"),  # median age
    ('B08301', 'B08301010'),  # Means of transportation to work: Public transportation (excluding taxicab)
]

# Uses only first 100 rows for testing purposes. (comment out when compiling final dataset)
df=df.head(100)

# Example usage
merge_df = fetch_multiple_no_moe(df, "geoid", variables)

print('heading: \n', merge_df.head())