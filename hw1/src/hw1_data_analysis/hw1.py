from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


# The CSV file is in the same directory as this Python script.
data_path = Path(__file__).with_name("bicycle_data.csv")

# Read the CSV file into a pandas DataFrame.
df = pd.read_csv(data_path)

# The Date column is stored as text and will be converted to datetime.
# The Total, West Sidewalk, and East Sidewalk columns are numeric bicycle counts. 
# Pandas reads them as float64 because missing values are represented as NaN.

print("Columns:")
print(df.columns.tolist())

print("\nFirst five rows:")
print(df.head())

print("\nOriginal data types:")
print(df.dtypes)


# Column names for the two directional bicycle counts.
east_col = (
    "Fremont Bridge Sidewalks, south of N 34th St "
    "Cyclist East Sidewalk"
)
west_col = (
    "Fremont Bridge Sidewalks, south of N 34th St "
    "Cyclist West Sidewalk"
)

# Convert Date strings such as "10/02/2012 01:00:00 PM" into pandas datetime values.
df["Date"] = pd.to_datetime(
    df["Date"],
    format="%m/%d/%Y %I:%M:%S %p",
)

# Add the combined bicycle count, hour of day, and year.
df["total_count"] = df[east_col] + df[west_col]
df["hour"] = df["Date"].dt.hour
df["year"] = df["Date"].dt.year

print("\nData with the new columns:")
print(df[["Date", "total_count", "hour", "year"]].head())


# Create a DataFrame containing only records from 2016.
df_2016 = df.loc[df["year"] == 2016].copy()

# A time point is missing a count if either directional count is missing.
missing_rows = df_2016[[east_col, west_col]].isna().any(axis=1)
missing_time_points = int(missing_rows.sum())

print(f"\nNumber of rows in 2016: {len(df_2016)}")
print(f"2016 time points with missing counts: {missing_time_points}")

# In the provided dataset, 1 time point in 2016 has a missing count in at least one direction.

# Remove time points with a missing East or West count.
df_2016_clean = df_2016.loc[~missing_rows].copy()

# Recalculate the combined count in the cleaned 2016 DataFrame.
df_2016_clean["total_count"] = (
    df_2016_clean[east_col] + df_2016_clean[west_col]
)

print(
    "Rows after removing missing counts: "
    f"{len(df_2016_clean)}"
)


# Calculate the average total bicycle count for each hour of the day.
hourly_average = (
    df_2016_clean.groupby("hour")["total_count"].mean()
)

print("\nAverage total bicycle count by hour:")
print(hourly_average)


# Plot the average count for each hour and save the figure.
ax = hourly_average.plot(kind="bar", figsize=(10, 6))
ax.set_title("Average Bicycle Counts by Hour in 2016")
ax.set_xlabel("Hour of Day")
ax.set_ylabel("Average Total Bicycle Count")
ax.set_xticks(range(24))
ax.set_xticklabels(
    [f"{hour:02d}:00" for hour in range(24)],
    rotation=45,
    ha="right",
)

plt.tight_layout()
plot_path = Path(__file__).with_name("counts_by_hour.png")
plt.savefig(plot_path, dpi=300)
plt.close()

print(f"\nPlot saved to: {plot_path}")


# Find the hour with the highest average total bicycle count.
busiest_hour = int(hourly_average.idxmax())

# For the provided dataset, the busiest average hour in 2016 is 17:00.
print(f"Average busiest hour: {busiest_hour:02d}:00")
print(
    "Average count during that hour: "
    f"{hourly_average.loc[busiest_hour]:.2f}"
)