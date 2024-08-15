

import pandas as pd
from typing import List, Dict
import json

class PowerMarketData:
    #---------------------------------------------------------
    def __init__(self, graph_config=None):
        self.data_frames: Dict[str, pd.DataFrame] = {}
        self.meta_data: Dict[str, pd.DataFrame] = {}
        self.graph_config = graph_config
        #self.api_client = api_client
        
        if self.graph_config:
            self.graph_config.apply_config()
    #---------------------------------------------------------
    def load_data(self, data_sources: Dict[str, str]):
        for key, path in data_sources.items():
            df = pd.read_csv(path)
            self.data_frames[key] = df
            print(f"Loaded {key} from {path}")
    #---------------------------------------------------------
    def load_meta_data(self, meta_data_sources: Dict[str, str]):
        for key, path in meta_data_sources.items():
            df = pd.read_csv(path)
            self.meta_data[key] = df
            print(f"Loaded meta data {key} from {path}")
    #---------------------------------------------------------
    def merge_data_frames(self):
        merged_df = None
        for key, df in self.data_frames.items():
            if merged_df is None:
                merged_df = df
            else:
                merged_df = pd.merge(merged_df, df, on='DateTime', how='outer')
        self.data_frames['merged'] = merged_df
        print("Merged all data frames into one")
    #---------------------------------------------------------
    def convert_column_headers(self):
        for key, df in self.data_frames.items():
            df.columns = df.columns.str.upper().str.replace(' ', '_')
            self.data_frames[key] = df
            print(f"Converted column headers for {key}")
    #---------------------------------------------------------
    def standardize_date_columns(self):
        for key, df in self.data_frames.items():
            for col in df.columns:
                if 'DATE' in col.upper():
                    df[col] = pd.to_datetime(df[col])
                    df.set_index(col, inplace=True)
                    self.data_frames[key] = df
                    print(f"Standardized date column for {key}")
                    break
    #---------------------------------------------------------            
    def standardize_date_time_columns(self, data_sources: Dict[str, Dict[str, str]], desired_format: str = '%m/%d/%Y %H:%M'):
        for key, config in data_sources.items():
            df = self.data_frames[key]
            date_format = config['date_format']
            date_col = config['date_col']
            
            # Convert 'Date Time' column to datetime64[ns] using the current format
            df[date_col] = pd.to_datetime(df[date_col], format=date_format, errors='coerce')
            
            # Standardize 'Date Time' column to the desired format
            df[date_col] = df[date_col].dt.strftime(desired_format)
            
            # Convert back to datetime to set as index
            df[date_col] = pd.to_datetime(df[date_col], format=desired_format)
            
            # Set 'Date Time' as index while retaining the column
            df.set_index(date_col, inplace=True, drop=False)
            
            self.data_frames[key] = df  # Update the processed DataFrame
            print(f"Standardized date column for {key}")
    #---------------------------------------------------------
    def aggregate_annual_files(self, file_paths: List[str], key: str):
        all_data = []
        for path in file_paths:
            df = pd.read_csv(path)
            all_data.append(df)
            print(f"Loaded {path}")

        aggregated_data = pd.concat(all_data, ignore_index=True)
        self.data_frames[key] = aggregated_data
        print(f"Aggregated data into {key}")
    #---------------------------------------------------------
    def serialize_merit_order_data(self, merit_order_key: str):
        merit_order_df = self.data_frames[merit_order_key]
        merit_order_df['MeritOrderData'] = merit_order_df.apply(lambda row: row.to_json(), axis=1)
        merit_order_df = merit_order_df[['DateTime', 'MeritOrderData']]
        self.data_frames[merit_order_key] = merit_order_df
        print(f"Serialized merit order data for {merit_order_key}")
    #---------------------------------------------------------
    def clean_data(self):
        for key, df in self.data_frames.items():
            df.dropna(inplace=True)  # Drop rows with missing values
            df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)  # Strip whitespace
            self.data_frames[key] = df
            print(f"Cleaned data for {key}")
    #---------------------------------------------------------
    def preprocess_data_frames(self, datetime_col='DateTime'):
        """
        Preprocess the provided data frames for analysis.
        """
        #..................................................................
        def standardize_index(df):
            if datetime_col in df.columns:
                df[datetime_col] = pd.to_datetime(df[datetime_col], errors='coerce')
                df.set_index(datetime_col, inplace=True)
            elif not pd.api.types.is_datetime64_any_dtype(df.index):
                df.index = pd.to_datetime(df.index, errors='coerce')
            return df
        #..................................................................
        def find_missing_hours(data_frames_dict):
            """
            Find missing hours in each data frame.
            """
            missing_hours = {}
            for name, df in data_frames_dict.items():
                full_range = pd.date_range(start=df.index.min(), end=df.index.max(), freq='H')
                missing_hours[name] = full_range.difference(df.index)
            return missing_hours
        #..................................................................
        def handle_dst_and_missing_data(data_frames_dict):
            updated_dataframes = {}
            duplicate_info = {}
            missing_hours = find_missing_hours(data_frames_dict)
            for name, df in data_frames_dict.items():
                try:
                    modified_df = df.copy()
                    modified_df = modified_df[~modified_df.index.duplicated(keep='first')]
                    for missing_hour in missing_hours[name]:
                        previous_hour = missing_hour - pd.Timedelta(hours=1)
                        if previous_hour in modified_df.index:
                            previous_hour_data = modified_df.loc[previous_hour]
                            modified_df.loc[missing_hour] = previous_hour_data
                    modified_df.sort_index(inplace=True)
                    modified_df = modified_df.asfreq('h', method='ffill')
                    updated_dataframes[name] = modified_df
                    duplicates = modified_df[modified_df.index.duplicated(keep=False)]
                    if not duplicates.empty:
                        duplicate_info[name] = duplicates
                except Exception as e:
                    print(f"An error occurred with DataFrame: {name}")
                    print(f"Error: {e}")
            missing_hours = find_missing_hours(updated_dataframes)
            return updated_dataframes, duplicate_info, missing_hours
        #..................................................................
        def align_data_frames(data_frames_dict):
            max_end_date = min(df.index.max() for df in data_frames_dict.values())
            aligned_data_frames_dict = {}
            for name, df in data_frames_dict.items():
                aligned_df = df.loc[:max_end_date]
                aligned_data_frames_dict[name] = aligned_df
            return aligned_data_frames_dict
        #..................................................................
        def check_missing_indices(data_frames):
            missing_indices_info = {}
            for i, df1 in enumerate(data_frames):
                for j, df2 in enumerate(data_frames):
                    if i != j:
                        key = (f"df{i+1}", f"df{j+1}")
                        missing_indices_info[key] = {
                            'missing_in_df1': df2.index.difference(df1.index),
                            'missing_in_df2': df1.index.difference(df2.index)
                        }
            return missing_indices_info
        #..................................................................
        def identify_and_print_duplicates(data_frames_dict):
            for name, df in data_frames_dict.items():
                if df.index.duplicated().any():
                    duplicates = df[df.index.duplicated(keep=False)]
                    print(f" Found duplicates in {name} based on index:")
                    print(duplicates)
                else:
                    print(f" No duplicates in {name} based on index:")
                    print("*" * 90)
        #..................................................................
        def check_24_hour_intervals(data_frames_dict):
            for name, df in data_frames_dict.items():
                daily_counts = df.groupby(df.index.date).count()
                row_counts = daily_counts.sum(axis=1)
                days_with_incorrect_counts = row_counts[row_counts != 24]
                total_missing_hours = sum(24 - count for count in days_with_incorrect_counts)
                print(f"Total missing hours in {name}: {total_missing_hours}")
                print("*" * 90)
        #..................................................................
        def process_each_data_frame(data_frames_dict):
            updated_dataframes = {}
            print("Starting Step 2a")
            updated_dataframes, duplicate_info, missing_hours = handle_dst_and_missing_data(data_frames_dict)
            print(f" Missing Hour Check at the end of handle_dst_and_missing_data() = {missing_hours}")

            for name in updated_dataframes:
                if name in duplicate_info:
                    print(f"Duplicate Hour Check for {name} at the end of handle_dst_and_missing_data():")
                    print(duplicate_info[name])
                else:
                    print(f"No duplicates found in {name} after processing.")
            print("*" * 90)
            print("Completed Step 2a: Each data frame has been processed for missing data, duplicates and DST.")
            
            for name, df in updated_dataframes.items():
                try:
                    print(f" Checking {name} for missing date-times:")
                    df_copy = df.copy()
                    print(f" Starting Step 2b for {name}")
                    df_copy = standardize_index(df_copy)
                    print(f" Completed Step 2b: {name} has been processed for standardized index")
                    print(f" Starting Step 2c for {name}")
                    updated_dataframes[name] = df_copy
                    print(f" Completed Step 2c: {name} returned to proceed to Step 3")
                    print("*" * 90)
                except Exception as e:
                    print(f"An error occurred with DataFrame: {name}")
                    print(f"Error: {e}")
                    break
                
            return updated_dataframes
        #..................................................................
        print("Starting Step 1")
        missing_indices_info_before = check_missing_indices(list(self.data_frames.values()))
        for key, value in missing_indices_info_before.items():
            print(f"Initial missing indices between {key[0]} and {key[1]}:", value)
        print("Completed Step 1: Each data frame has been processed for missing indices.")
        print("*" * 90)

        print("Starting Step 2")
        processed_data_frames_dict = process_each_data_frame(self.data_frames)

        print("Starting Step 2.5")
        identify_and_print_duplicates(processed_data_frames_dict)
        print("Completed Step 2.5: Each data frame has been checked again for duplicates.")

        print("Starting Step 3")
        aligned_data_frames_dict = align_data_frames(processed_data_frames_dict)
        print("Completed Step 3: Each data frame has been processed for alignment.")

        print("Starting Step 4")
        identify_and_print_duplicates(aligned_data_frames_dict)
        print("Completed Step 4: Each data frame has been checked again for duplicates.")

        print("Starting Step 5")
        check_24_hour_intervals(aligned_data_frames_dict)
        print("Completed Step 5: Each data frame has been checked to ensure each day has a 24-hour interval.")

        print("Starting Step 6")
        missing_indices_info_after = check_missing_indices(list(aligned_data_frames_dict.values()))
        for key, value in missing_indices_info_after.items():
            print(f"Final missing indices between {key[0]} and {key[1]}:", value)
        print("Completed Step 6: Each data frame has been checked for missing indices.")
        print("*" * 90)

        self.data_frames = aligned_data_frames_dict
        return self.data_frames
    #-------------------------------------------------------
    def process_data(self):
        for key, df in self.data_frames.items():
            if 'HOURLY' in key.upper():
                df['DATE'] = df.index.date
                df['HOUR'] = df.index.hour
                # Example of a simple statistical summary
                df['MEAN'] = df.mean(axis=1)
                df['STD'] = df.std(axis=1)
                self.data_frames[key] = df
                print(f"Processed data for {key}")
    #-------------------------------------------------------
    def summarize_data(self):
        summaries = {}
        for key, df in self.data_frames.items():
            if 'HOURLY' in key.upper():
                monthly_summary = df.resample('M').mean()
                quarterly_summary = df.resample('Q').mean()
                annual_summary = df.resample('A').mean()
                summaries[key] = {
                    'monthly': monthly_summary,
                    'quarterly': quarterly_summary,
                    'annual': annual_summary
                }
                print(f"Summarized data for {key}")
        self.summaries = summaries
    #-------------------------------------------------------
    def create_visualizations(self):
        for key, df in self.data_frames.items():
            if 'HOURLY' in key.upper():
                plt.figure(figsize=(12, 6))
                df['MEAN'].plot()
                plt.title(f'Mean Hourly {key}')
                plt.xlabel('Date')
                plt.ylabel('Mean Value')
                plt.savefig(f'{key}_mean_hourly.png')
                plt.close()
                print(f"Created visualization for {key}")
    #-------------------------------------------------------
    def filter_data(self, start_date=None, end_date=None, asset_id=None, fuel_type=None, tech_type=None):
        filtered_data = {}
        for key, df in self.data_frames.items():
            if start_date and end_date:
                df = df[(df.index >= start_date) & (df.index <= end_date)]
            if asset_id:
                df = df[df['ASSET_ID'] == asset_id]
            if fuel_type:
                df = df[df['FUEL_TYPE'] == fuel_type]
            if tech_type:
                df = df[df['TECH_TYPE'] == tech_type]
            filtered_data[key] = df
            print(f"Filtered data for {key} based on given criteria")
        return filtered_data
    #-------------------------------------------------------
    def create_animation(self, key: str, column: str, title: str, save_path=None):
        if key in self.data_frames:
            data = self.data_frames[key]
            anim = Animation(data, column, title)
            anim.start_animation(save_path)
            print(f"Created animation for {key} on column {column}")
        else:
            print(f"No data found for key: {key}")
    #-------------------------------------------------------
    def export_data(self, path: str):
        # Export consolidated data to CSV
        for key, df in self.data_frames.items():
            df.to_csv(f"{path}/{key}.csv")
            print(f"Exported {key} to {path}/{key}.csv")
    #-------------------------------------------------------
    def populate_sql(self, connection_string: str):
        # Implement your SQL population logic here
        pass
    #-------------------------------------------------------
    def export_to_sql(self, db_path: str):
        import sqlite3
        conn = sqlite3.connect(db_path)
        for key, df in self.data_frames.items():
            df.to_sql(key, conn, if_exists='replace', index=False)
            print(f"Exported {key} to SQL database {db_path}")
        conn.close()
        
        
# Utility functions for managing metadata
def load_metadata(json_file: str) -> Dict:
    with open(json_file, 'r') as file:
        return json.load(file)

def save_metadata(json_file: str, metadata: Dict):
    with open(json_file, 'w') as file:
        json.dump(metadata, file, indent=4)

def create_data_object_existing_file(base_path: str, sub_folder: str, json_file: str):
    metadata = load_metadata(json_file)
    data_sources = metadata['data_sources']
    
    # Create PowerMarketData instance
    power_market_data = PowerMarketData()
    power_market_data.load_data(data_sources)
    power_market_data.convert_column_headers()
    power_market_data.standardize_date_columns(data_sources)
    power_market_data.merge_data_frames()
    
    return power_market_data

def create_data_object_new_file(base_path: str, sub_folder: str, json_file: str, new_file: str, date_format: str, date_col: str):
    metadata = load_metadata(json_file)
    data_sources = metadata['data_sources']
    
    new_key = new_file.split('.')[0]  # Use the file name (without extension) as the key
    new_path = f"{base_path}/{sub_folder}/{new_file}"
    
    # Add new file info to data_sources
    data_sources[new_key] = {
        'path': new_path,
        'date_format': date_format,
        'date_col': date_col
    }
    
    # Save updated metadata
    save_metadata(json_file, metadata)
    
    # Create PowerMarketData instance
    power_market_data = PowerMarketData()
    power_market_data.load_data(data_sources)
    power_market_data.convert_column_headers()
    power_market_data.standardize_date_columns(data_sources)
    power_market_data.merge_data_frames()
    
    return power_market_data

def purge_metadata(json_file: str):
    metadata = {"data_sources": {}}
    save_metadata(json_file, metadata)
    print("Purged metadata")
###################################################
# Example usage
json_file = 'file_data.json'

# Create a PowerMarketData instance for existing files
existing_data_cls_obj = create_data_object_existing_file(r'C:\Users\Rob_Kaz\OneDrive\Documents\Rob Personal Documents\Python\AB Electricity Sector Stats', '', json_file)

# Add a new data file to the project and create a PowerMarketData instance
new_data_cls_obj = create_data_object_new_file('base_path', 'sub_folder', json_file, 'new_file.csv', '%Y-%m-%d %H:%M', 'Date Time')

# Purge metadata
purge_metadata(json_file)