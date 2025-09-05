# HIT137 Assignment 2 - Question 2
#
# Group Name: SYDN 28
# Group Members:
# Krish Rajbhandari - S395754
# Noor-E-Sefat Ahmed - S394047
# Mehedi Hasan - S395003
# Suyog Kadariya - S393829

# This program reads temperature CSVs from the "temperatures" folder.
# It calculates:
#   1) Average seasonal temperatures
#   2) The station with the largest temperature range
#   3) The most stable and most variable stations
#   4) It then writes results to three text files.

import os
import pandas as pd

# Dictionary: month name → number (like in our Week 4 lecture)
MONTH_TO_NUM = {
    "January": 1, "February": 2, "March": 3,
    "April": 4, "May": 5, "June": 6,
    "July": 7, "August": 8, "September": 9,
    "October": 10, "November": 11, "December": 12
}

# Function: decide season from month number
def month_to_season(m):
    if m in (12, 1, 2):
        return "Summer"
    elif m in (3, 4, 5):
        return "Autumn"
    elif m in (6, 7, 8):
        return "Winter"
    else:
        return "Spring"

# Function: read all csv files and return one dataframe
def load_data():
    folder = "temperatures"
    files = [f for f in os.listdir(folder) if f.endswith(".csv")]
    frames = []

    for f in files:
        df = pd.read_csv(os.path.join(folder, f))
        # melt = turn months into rows
        months = [m for m in MONTH_TO_NUM if m in df.columns]
        if "Station" in df.columns:
            station_col = "Station"
        elif "STATION_NAME" in df.columns:
            station_col = "STATION_NAME"
        else:
            continue  # skip if no station column
        long = df.melt(id_vars=[station_col],
                       value_vars=months,
                       var_name="MonthName",
                       value_name="Temperature")
        long["Station"] = long[station_col]
        long["Month"] = long["MonthName"].map(MONTH_TO_NUM)
        long = long.dropna(subset=["Temperature"])
        frames.append(long[["Station","Month","Temperature"]])

    return pd.concat(frames, ignore_index=True)

# Function: write outputs
def write_outputs(data):
    # 1) Average seasonal temps
    data["Season"] = data["Month"].apply(month_to_season)
    seasonal = data.groupby("Season")["Temperature"].mean().round(1)
    with open("average_temp.txt", "w") as f:
        for s, v in seasonal.items():
            f.write(f"{s}: {v}°C\n")

    # 2) Largest temperature range
    stats = data.groupby("Station")["Temperature"].agg(["max","min"])
    stats["range"] = stats["max"] - stats["min"]
    max_range = stats["range"].max()
    winners = stats[stats["range"] == max_range]
    with open("largest_temp_range_station.txt", "w") as f:
        for st, row in winners.iterrows():
            f.write(f"{st}: Range {row['range']:.1f}°C\n")

    # 3) Stability (std dev)
    stds = data.groupby("Station")["Temperature"].std()
    most_stable = stds[stds == stds.min()]
    most_variable = stds[stds == stds.max()]
    with open("temperature_stability_stations.txt", "w") as f:
        for st, v in most_stable.items():
            f.write(f"Most Stable: {st} (StdDev {v:.1f}°C)\n")
        for st, v in most_variable.items():
            f.write(f"Most Variable: {st} (StdDev {v:.1f}°C)\n")

# Main function
def main():
    print("Loading temperature data...")
    data = load_data()
    print("Calculating results...")
    write_outputs(data)
    print("Done. Results saved.")

# Call main
if __name__ == "__main__":
    main()
