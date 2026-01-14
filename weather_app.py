import pandas as pd
import glob
import math
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(script_dir, "temperatures")

weather_files = sorted(glob.glob(os.path.join(data_path, "stations_group_*.csv")))

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
    season_totals = {season: [] for season in month_groups.keys()}
    
    for df in dataframes:
        for group_name, group_months in month_groups.items():
            season_avg = df[group_months].mean().mean()
            season_totals[group_name].append(season_avg)

    print("\n" + "="*60)
    print("SEASONAL AVERAGE TEMPERATURES - ALL FILES")
    print("="*60)
    
    with open(os.path.join(data_path, "average_temp.txt"), "w") as f:
        f.write("SEASONAL AVERAGE TEMPERATURES\n" + "="*30 + "\n")
        for season, values in season_totals.items():
            overall_avg = math.ceil(sum(values) / len(values))
            output = f"In {season} the avg temp was {overall_avg}°C"
            print(output)
            f.write(output + "\n")

def analyze_temperature_difference(combined_df):
    if 'Temp_Difference' in combined_df.columns:
        print("\n" + "="*60)
        print("TEMPERATURE DIFFERENCE - ALL FILES")
        print("="*60)
        
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
    if 's_d' in combined_df.columns:
        print("\n" + "="*60)
        print("STANDARD DEVIATION - ALL FILES")
        print("="*60)
        
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

all_dataframes = []

if not weather_files:
    print(f"Error: No files found in {data_path}")
else:
    for file in weather_files:
        df = pd.read_csv(file)
        df['Temp_Difference'] = df[months].max(axis=1) - df[months].min(axis=1)
        df['s_d'] = df[months].std(axis=1)
        all_dataframes.append(df)

    combined_df = pd.concat(all_dataframes, ignore_index=True)
    calculate_seasonal_averages(all_dataframes)
    analyze_temperature_difference(combined_df)
    analyze_standard_deviation(combined_df)

print("\n" + "="*60)