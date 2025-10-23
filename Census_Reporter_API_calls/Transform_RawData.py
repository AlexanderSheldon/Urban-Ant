import pandas as pd
import numpy as np

df = pd.read_csv('Census_Reporter_API_calls/RawData.csv')

# ---- configure once ----
MODES = {
    "pt": "Public transportation",
    "drive": "Driving Alone",
}
BINS = [
    "Less than 10 minutes",
    "10 to 14 minutes",
    "15 to 19 minutes",
    "20 to 24 minutes",
    "25 to 29 minutes",
    "30 to 34 minutes",
    "35 to 44 minutes",
    "45 to 59 minutes",
    "60 or more minutes",
]
MIDPOINTS = np.array([5, 12, 17, 22, 27, 32, 39.5, 52, 70], float)
BOUNDS = np.array([
    (0,10),(10,15),(15,20),(20,25),(25,30),
    (30,35),(35,45),(45,60),(60,np.inf)
], dtype=object)

def add_commute_summaries(df: pd.DataFrame, key: str, label: str) -> None:
    """Appends summary columns for one mode in-place (suffix = key)."""
    cols = [f"{b} Travel Time to Work via {label}" for b in BINS]
    total = f"Total Travel Time to Work via {label}"

    df[cols + [total]] = df[cols + [total]].apply(pd.to_numeric, errors="coerce").fillna(0.0)
    denom = df[total].replace(0, np.nan)

    # average minutes (weighted midpoints)
    df[f"avg_minutes_{key}"] = (df[cols].mul(MIDPOINTS, axis=1).sum(axis=1)) / denom

    # median via simple within-bin interpolation
    def _median(row):
        c = row.cumsum().to_numpy()
        T = c[-1]
        if T <= 0: return np.nan
        t = 0.5 * T
        i = int(np.searchsorted(c, t, "left"))
        lo, hi = BOUNDS[i]
        prev = 0 if i == 0 else c[i-1]
        in_bin = row.iat[i]
        if np.isinf(hi) or in_bin == 0: return float(lo)
        return float(lo + (t - prev) / in_bin * (hi - lo))
    df[f"median_minutes_{key}"] = df[cols].apply(_median, axis=1)

    # thresholds & 3-bin collapse
    short, medium, longb = cols[:5], cols[5:7], cols[7:]
    df[f"p_under_30_{key}"] = df[short].sum(axis=1) / denom
    df[f"p_45_plus_{key}"]  = df[longb].sum(axis=1) / denom
    df[f"p_60_plus_{key}"]  = df[[cols[-1]]].sum(axis=1) / denom

    df[f"share_short_{key}"]  = df[short].sum(axis=1) / denom
    df[f"share_medium_{key}"] = df[medium].sum(axis=1) / denom
    df[f"share_long_{key}"]   = df[longb].sum(axis=1) / denom

# ---- use on your DataFrame `df` ----
for k, lbl in MODES.items():
    add_commute_summaries(df, k, lbl)

# Example: keep just the new columns (plus an id)
keep = ["geoid"] + [c for c in df.columns if c.endswith("_pt") or c.endswith("_drive")]
df_out = df[keep]

print(df.head())
print(df.columns)

df.to_csv('/workspaces/Urban-Ant/Census_Reporter_API_calls/Transformed_Data.csv', index = False)