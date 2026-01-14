"""
CLIMATE DATA ANALYSIS TOOL
--------------------------
This script processes multiple CSV files to calculate seasonal temperature 
averages, identify extreme temperature ranges, and evaluate climate stability.
"""

import pandas as pd
import glob
import math
import os

# --- ENVIRONMENT SETUP ---
# Detects the current folder and locates the 'temperatures' sub-folder
script_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(script_dir, "temperatures")

# Collects all station data files ending in .csv
# Note: Ensure the folder name does not contain square brackets []
weather_files = sorted(glob.glob(os.path.join(data_path, "stations_group_*.csv")))

# Lists for organizing months and seasonal categories
months = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]

month_groups = {
    "Summer": ["December", "January", "February"],
    "Autumn": ["March", "April", "May"],
    "Winter": ["June", "July", "August"],
    "Spring": ["September", "October", "November"]
}

def calculate_seasonal_averages(dataframes):
    """
    Computes the mean temperature for each season across all files.
    Saves the final rounded averages to 'average_temp.txt'.
    """
    season_totals = {season: [] for season in month_groups.keys()}
    
    for df in dataframes:
        for group_name, group_months in month_groups.items():
            # Averages data across the months in each season
            season_avg = df[group_months].mean().mean()
            season_totals[group_name].append(season_avg)

    print("\n" + "="*60)
    print("SEASONAL AVERAGE TEMPERATURES - ALL FILES")
    print("="*60)
    
    with open(os.path.join(data_path, "average_temp.txt"), "w") as f:
        f.write("SEASONAL AVERAGE TEMPERATURES\n" + "="*30 + "\n")
        for season, values in season_totals.items():
            # Calculates the grand mean and rounds up for the final output
            overall_avg = math.ceil(sum(values) / len(values))
            output = f"In {season} the avg temp was {overall_avg}°C"
            print(output)
            f.write(output + "\n")

def analyze_temperature_difference(combined_df):
    """
    Identifies stations with the largest gap between hottest and coldest months.
    Saves the results to 'largest_temp_range_station.txt'.
    """
    if 'Temp_Difference' in combined_df.columns:
        print("\n" + "="*60)
        print("TEMPERATURE DIFFERENCE - ALL FILES")
        print("="*60)
        
        # Finds the highest temperature range in the dataset
        max_diff = combined_df["Temp_Difference"].max()
        max_diff_rows = combined_df[combined_df["Temp_Difference"] == max_diff]
        
        print("Stations with largest temperature difference:")
        print("-"*60)
    
        with open(os.path.join(data_path, "largest_temp_range_station.txt"), "w") as f:
            f.write("STATION WITH LARGEST TEMPERATURE DIFFERENCE\n" + "="*45 + "\n")
            for _, row in max_diff_rows.iterrows():
                output = f"Station: {row['STATION_NAME']} | Difference: {math.ceil(row['Temp_Difference'])} °C"
                print(output)
                f.write(output + "\n")

def analyze_standard_deviation(combined_df):
    """
    Analyzes temperature stability using Standard Deviation (SD).
    Identifies the most volatile and most stable stations.
    """
    if 's_d' in combined_df.columns:
        print("\n" + "="*60)
        print("STANDARD DEVIATION - ALL FILES")
        print("="*60)
        
        # Finds the maximum and minimum standard deviation values
        max_sd_value = combined_df["s_d"].max()
        min_sd_value = combined_df["s_d"].min()
        max_sd_rows = combined_df[combined_df["s_d"] == max_sd_value]
        min_sd_rows = combined_df[combined_df["s_d"] == min_sd_value]
        
        with open(os.path.join(data_path, "temperature_stability_stations.txt"), "w") as f:
            f.write("TEMPERATURE STABILITY (Standard Deviation)\n" + "="*45 + "\n")
            
            print("Stations with largest SD:")
            print("-"*60)
            for _, row in max_sd_rows.iterrows():
                stn_id = row.get("STN_ID")
                output = f"Station: {row['STATION_NAME']} | STN_ID: {stn_id} | SD: {row['s_d']:.2f}°C"
                print(output)
                f.write("Largest SD: " + output + "\n")
            
            print("\nStations with smallest SD:")
            print("-"*60)
            for _, row in min_sd_rows.iterrows():
                stn_id = row.get("STN_ID")
                output = f"Station: {row['STATION_NAME']} | STN_ID: {stn_id} | SD: {row['s_d']:.2f}°C"
                print(output)
                f.write("Smallest SD: " + output + "\n")

# --- DATA PROCESSING PIPELINE ---
all_dataframes = []

if not weather_files:
    print(f"Error: No files found in {data_path}")
else:
    # Loads each CSV and calculates range and standard deviation per row
    for file in weather_files:
        df = pd.read_csv(file)
        df['Temp_Difference'] = df[months].max(axis=1) - df[months].min(axis=1)
        df['s_d'] = df[months].std(axis=1)
        all_dataframes.append(df)

    # Merges all files into one master table and runs analysis
    combined_df = pd.concat(all_dataframes, ignore_index=True)
    calculate_seasonal_averages(all_dataframes)
    analyze_temperature_difference(combined_df)
    analyze_standard_deviation(combined_df)

print("\n" + "="*60)
