# HIT137 Assignment 2 - Question 2 
# Student: Noor-E-Sefat Ahmed, ID: S394047

import os, re
import pandas as pd

TEMPS_DIR = "temperatures"

OUT_AVG = "average_temp.txt"
OUT_RANGE = "largest_temp_range_station.txt"
OUT_STAB = "temperature_stability_stations.txt"

MONTHS = ["January","February","March","April","May","June",
          "July","August","September","October","November","December"]
MONTH_TO_NUM = {m:i+1 for i,m in enumerate(MONTHS)}

def detect_year_from_filename(fname: str) -> int | None:
    m = re.search(r"(19|20)\d{2}", fname)
    return int(m.group(0)) if m else None

def station_col_name(cols: list[str]) -> str | None:
    # prefer exact if present
    for c in ["STATION_NAME","Station_Name","Station","station_name","station","SITE_NAME","Site"]:
        if c in cols:
            return c
    # fallback: anything containing 'station' or 'site'
    for c in cols:
        cl = c.lower()
        if "station" in cl or "site" in cl:
            return c
    return None

def load_wide_folder(folder: str) -> pd.DataFrame:
    """
    Expect files with columns like:
      STATION_NAME, STN_ID, LAT, LON, January,...,December
    Returns long table: Station | Year | Month | Temperature
    """
    files = sorted([f for f in os.listdir(folder) if f.lower().endswith(".csv")])
    if not files:
        raise SystemExit("[Q2] ERROR: No .csv files found in temperatures/")

    frames = []
    used = 0
    for fname in files:
        path = os.path.join(folder, fname)
        try:
            df0 = pd.read_csv(path)
        except Exception as e:
            print(f"[Q2] SKIP {fname:>25s}  read error: {e}")
            continue

        cols = list(df0.columns)
        # check for monthly columns
        has_months = any(m in cols for m in MONTHS)
        sc = station_col_name(cols)
        yr = detect_year_from_filename(fname)

        if not has_months or not sc or yr is None:
            print(f"[Q2] SKIP {fname:>25s}  reason: months/station/year missing "
                  f"(has_months={has_months}, station={sc}, year={yr})")
            continue

        keep = [sc] + [m for m in MONTHS if m in cols]
        wide = df0[keep].copy()
        long = wide.melt(id_vars=[sc], value_vars=[m for m in MONTHS if m in wide.columns],
                         var_name="MonthName", value_name="Temperature")
        long["Station"] = long[sc].astype(str).str.strip()
        long["Year"] = yr
        long["Month"] = long["MonthName"].map(MONTH_TO_NUM)
        long["Temperature"] = pd.to_numeric(long["Temperature"], errors="coerce")
        before = len(long)
        long = long.dropna(subset=["Temperature"])
        long = long[["Station","Year","Month","Temperature"]]
        frames.append(long)
        used += 1
        print(f"[Q2] OK   {fname:>25s}  schema:wide  rows_in:{before:5d}  kept:{len(long):5d}")

    if not frames:
        raise SystemExit("[Q2] ERROR: No usable .csv files after parsing.")

    print(f"[Q2] Loaded {used}/{len(files)} csv files successfully.")
    return pd.concat(frames, ignore_index=True)

def month_to_season(m: int) -> str:
    if m in (12,1,2): return "Summer"
    if m in (3,4,5):  return "Autumn"
    if m in (6,7,8):  return "Winter"
    return "Spring"

def write_outputs(data: pd.DataFrame):
    # 1) Seasonal averages across all stations/years
    tmp = data.copy()
    tmp["Season"] = tmp["Month"].apply(month_to_season)
    seasonal = tmp.groupby("Season")["Temperature"].mean().round(1)
    seasonal = seasonal.reindex(["Summer","Autumn","Winter","Spring"])
    with open(OUT_AVG, "w", encoding="utf-8") as f:
        for s, v in seasonal.items():
            if pd.notna(v):
                f.write(f"{s}: {v:.1f}°C\n")
    print(f"[1/3] Wrote seasonal averages → {OUT_AVG}")

    # 2) Largest temp range per station
    agg = data.groupby("Station")["Temperature"].agg(["max","min"])
    agg["range"] = agg["max"] - agg["min"]
    maxr = agg["range"].max()
    winners = agg[agg["range"] == maxr].sort_index()
    with open(OUT_RANGE, "w", encoding="utf-8") as f:
        for station, row in winners.iterrows():
            f.write(f"{station}: Range {row['range']:.1f}°C "
                    f"(Max: {row['max']:.1f}°C, Min: {row['min']:.1f}°C)\n")
    print(f"[2/3] Wrote largest temp range stations → {OUT_RANGE}")

    # 3) Stability (std dev)
    stds = data.groupby("Station")["Temperature"].std(ddof=1)
    min_std, max_std = stds.min(), stds.max()
    most_stable = stds[stds == min_std].sort_index()
    most_variable = stds[stds == max_std].sort_index()
    with open(OUT_STAB, "w", encoding="utf-8") as f:
        for st, v in most_stable.items():
            f.write(f"Most Stable: {st}: StdDev {v:.1f}°C\n")
        for st, v in most_variable.items():
            f.write(f"Most Variable: {st}: StdDev {v:.1f}°C\n")
    print(f"[3/3] Wrote temperature stability stations → {OUT_STAB}")

def main():
    print("=== Q2 script v2 (wide-only) ===")
    print(f"Reading CSVs from: {TEMPS_DIR}/")
    data = load_wide_folder(TEMPS_DIR)
    write_outputs(data)
    print("Done.")

if __name__ == "__main__":
    main()
