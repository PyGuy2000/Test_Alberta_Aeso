
import shutil
from config import code_begin, code_end
import initializer as init #alias for initializer.py
import global_variables as gv #alias for global_variables.py
# from global_variables import(
# gbl_base_input_directory_global, 
# gbl_base_output_directory_global, 
# gbl_csv_folder, 
# gbl_image_folder)
import os
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker  # Import the ticker module
import copy
from pathlib import Path
import pandas as pd 
from pandas.tseries.holiday import AbstractHolidayCalendar, Holiday, USFederalHolidayCalendar
from datetime import time
import numpy as np
from tqdm import tqdm
import geopandas as gpd


code_begin()

############################################
# Helper Functions
############################################
def insert_header_footer(text_label, level, include_text = True):
    #Note level = 1 to 3
    #****************************
    #----------------------------
    #............................
    
    char1 = "*"
    char2 = "-"
    char3 = "."
    
    if include_text == False:
        text_label = ""
    else:
        text_label = text_label
    
    if level == 1:
        print(char1 *90)
        print(f"{text_label}")
        print(char1 *90)
        
    elif level == 2:
        print(char2 *90)
        print(f"{text_label}")
        print(char2 *90)
        
    elif level == 3:
        print(char3 *90)
        print(f"{text_label}")
        print(char3 *90)

    
    return


import re
'''
This function converst colkumn headers to an uppercae string, removes special characters and replaces spaces with underscores.

'''
def transform_strings(strings):
    transformed_strings = []
    for string in strings:
        # Convert to uppercase
        string = string.upper()
        # Remove special characters
        string = re.sub(r'[^A-Z0-9\s]', '', string)
        # Replace spaces with underscores
        string = re.sub(r'\s+', '_', string)
        transformed_strings.append(string)
    return transformed_strings


def convert_to_function_name(text):
    """
    Convert a given string to a valid function name in lowercase with underscores replacing spaces.
    
    Args:
    text (str): The input string to be converted.
    
    Returns:
    str: The converted function name.
    """
    function_name = text.strip().lower().replace(" ", "_").replace("-", "_").replace("*", "")
    return function_name + "()"

#------------------------------------------
# Function to automatically pick font color
def autopct_format(values):
    def inner_autopct(pct):
        total = sum(values)
        val = int(round(pct*total/100.0))
        color = 'white' if (pct < 50) else 'black'
        return '{p:.2f}%\n({v:d} MW)'.format(p=pct, v=val, c=color)
    return inner_autopct


#-------------------------------------------
# Load column headers from csv file
def load_columns_from_csv(df):
    columns = {}
    with open(file_path, mode='r') as infile:
        reader = csv.DictReader(infile)
        for row in reader:
            columns[row['column_name']] = row['value']
    return columns
#-------------------------------------------
# Load column headers from data frame
def load_column_names_from_df(df):
    columns = {}
    for column in df.columns:
        # Create a key for each column name
        key = f'{column.lower()}_column_hdr'
        # Add the key-value pair to the dictionary
        columns[key] = column
    return columns
#-------------------------------------------
# Function to remove folder contents at start-up and create csv and image folders to save data in.
def remove_folder_contents(folder):
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                remove_folder_contents(file_path)
                os.rmdir(file_path)
        except Exception as e:
            print(e)
#-------------------------------------------
def setup_directories():
    remove_folder_contents(init.gbl_base_output_directory_global)
    print(f" base_output_directory_global: {init.gbl_base_output_directory_global}")
    os.makedirs(os.path.join(init.gbl_base_output_directory_global, init.gbl_csv_folder), exist_ok=True)
    os.makedirs(os.path.join(init.gbl_base_output_directory_global, init.gbl_image_folder), exist_ok=True)


#remove_folder_contents(gbl_base_output_directory_global)
#print(f" base_output_directory_global: {gbl_base_output_directory_global}")

# Create CSV and Image folders
#os.makedirs(os.path.join(gbl_base_output_directory_global, gbl_csv_folder), exist_ok=True)
#os.makedirs(os.path.join(gbl_base_output_directory_global, gbl_image_folder), exist_ok=True)

#-------------------------------------------

# On/Off Peak Delineation Code
# Define Canadian holidays
class CanadianHolidayCalendar(AbstractHolidayCalendar):
    rules = [
        Holiday('New Year', month=1, day=1),
        # Add other Canadian holidays here
    ]
#-------------------------------------------
def save_to_image(df, filename):
    if init.gbl_ide_option == 'vscode':
        filename = filename + '.png'
        full_path = os.path.join(init.gbl_base_output_directory_global,filename)
        df.to_csv(full_path, index=True)
    elif init.gbl_ide_option == 'jupyter_notebook':
        pass

    elif init.gbl_ide_option == 'kaggle':
        pass
    return
#-------------------------------------------
def create_path(input_dir, filename, subfolder_name=''):
    # Use os.path.join for all components
    # os.path.join will handle empty strings appropriately by ignoring them
    full_path = os.path.normpath(os.path.join(input_dir, subfolder_name, filename))
    return full_path

#-------------------------------------------
def read_from_csv_input_folder(filename, subfolder_name=''):
    if init.gbl_ide_option == 'vscode':
        full_path = create_path(init.gbl_base_input_directory_global, filename, subfolder_name)
        print(f" full_path: {full_path}")
     # Check if the path exists
        if not os.path.exists(full_path):
            print("Error: The file does not exist at the specified path.")
            return None
        df = pd.read_csv(full_path, low_memory=False)
        
    elif init.gbl_ide_option == 'jupyter_notebook':
        # Additional code for Jupyter environment
        pass

    elif init.gbl_ide_option == 'kaggle':
        # Additional code for Kaggle environment
        full_path = create_path(init.gbl_base_input_directory_global, filename, subfolder_name)
        print(f" full_path: {full_path}")
         # Check if the path exists
#         if not os.path.exists(full_path):
#             print("Error: The file does not exist at the specified path.")
#             return None
        df = pd.read_csv(full_path, low_memory=False)

    # Check if the DataFrame is empty
    if df.empty:
        print("Error: The file is empty.")
        return None
    
    print(f" {filename} loaded from input folder...") 
    return df

#-------------------------------------------
def read_from_csv_output_folder(filename, subfolder_name=''):
    
    if gbl_ide_option == 'vscode':
        output_directory = os.path.join(init.gbl_base_output_directory_global, init.gbl_csv_folder)
        full_path = create_path(output_directory, filename)
        print(f" full_path: {full_path}")
     # Check if the path exists
        if not os.path.exists(full_path):
            print("Error: The file does not exist at the specified path.")
            return None
        df = pd.read_csv(full_path, low_memory=False)
        
    elif init.gbl_ide_option == 'jupyter_notebook':
        # Additional code for Jupyter environment
        pass

    elif init.gbl_ide_option == 'kaggle':
        full_path = create_path(init.gbl_base_output_directory_global, filename)
        print(f" full_path: {full_path}")
        df = pd.read_csv(full_path, low_memory=False)
    
    print(f" {filename} loaded from output folder...") 
    return df
#-------------------------------------------
def save_dataframe_to_csv(df, filename):
  
    if init.gbl_ide_option == 'vscode':
        output_directory = os.path.join(init.gbl_base_output_directory_global, init.gbl_csv_folder)
        full_path = create_path(output_directory, filename)
        print(f"print file path: {full_path}")
        
        # Ensure the directory exists, not the file itself
        directory = os.path.dirname(full_path)  # Get the directory path
        if not os.path.exists(directory):       # Check if directory exists
            os.makedirs(directory)              # Create the directory if it does not exist

        df.to_csv(full_path, index=True,header=True)        # Save the DataFrame to CSV
        print(f"{filename} saved to output folder...")

    elif init.gbl_ide_option == 'jupyter_notebook':
        pass

    elif init.gbl_ide_option == 'kaggle':
        full_path = create_path(init.gbl_base_output_directory_global, filename)
        print(f"print file path: {full_path}")
        
        # Ensure the directory exists, not the file itself
        directory = os.path.dirname(full_path)  # Get the directory path
        if not os.path.exists(directory):       # Check if directory exists
            os.makedirs(directory)              # Create the directory if it does not exist

        df.to_csv(full_path, index=True)        # Save the DataFrame to CSV
        print(f"{filename} saved to output folder...")
        
    return

#-------------------------------------------
# Function to label peak hours
def label_on_off_peak_hours(data):
    # Ensure the index is in datetime format (if not already)
    data.index = pd.to_datetime(data.index)

    # Get holidays for Canada
    calendar = CanadianHolidayCalendar()
    holidays = calendar.holidays(start=data.index.min(), end=data.index.max())

    # Initialize 'peak_status' column
    data['peak_status'] = 'Off-Peak'  # Default value

    # Define on-peak hours (example: 7 AM to 11 PM)
    on_peak_hours = [time(7, 0), time(23, 0)]

    # Label hours as On-Peak or Off-Peak
    for index, row in data.iterrows():
        current_time = index.time()  # Getting the time part of the index
        current_date = index.date()  # Getting the date part of the index
        day_of_week = index.dayofweek  # Monday=0, Sunday=6

        # Check if it's a weekday (Monday=0, Sunday=6)
        if day_of_week < 5:  # Monday to Friday
            if current_time >= on_peak_hours[0] and current_time <= on_peak_hours[1] and current_date not in holidays:
                data.at[index, 'peak_status'] = 'On-Peak'
        # For Saturday and Sunday, it's always Off-Peak, so no action needed as default is Off-Peak

    return data
#-------------------------------------------
# Function to calculate the steepest point and draw vertical lines (excluding extremes)
def plot_steepest_point(ax, x_values, y_values, exclusion_percentage):
    exclude_count = int(len(x_values) * exclusion_percentage / 100)
    
    # Exclude the first and last parts of the data
    slopes = np.diff(y_values[exclude_count:-exclude_count]) / np.diff(x_values[exclude_count:-exclude_count])
    max_slope_idx = np.argmax(np.abs(slopes)) + exclude_count
    
    # Steepest point
    x_steepest = x_values[max_slope_idx]
    
    # Draw vertical line
    ax.axvline(x=x_steepest, color='grey', linestyle='--', alpha=0.7)

#-------------------------------------------

def create_demand_heatmap(data, heatmap_title, y_label, x_label, total = None):
  

    # Divide the values by 1000 to represent them in GWh
    #year_month_result_table_in_gwh = year_month_result_table

    # Set the figure size
    plt.figure(figsize=(12, 8))
    
    if total == True:
        # Add a 'Total' column that sums the annual production across all Tech_Types for each year
        data['Total'] = data.sum(axis=1)
    
    # Create the heatmap for year_month_result_table_in_gwh with custom tick labels and GWh color strip
    ax = sns.heatmap(data, cmap='coolwarm_r', annot=True, fmt=',.0f', linewidths=0.5)

    # Rotate the year markers on the x-axis by 0 degrees (horizontal)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=0)

    # Rotate the week values on the y-axis by 0 degrees (horizontal)
    ax.set_yticklabels(ax.get_yticklabels(), rotation=0)

    # Set the title and labels
    chart_title = heatmap_title
    plt.title(chart_title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)

    # Customize the color bar labels to display in GWh
    cbar = ax.collections[0].colorbar
    cbar.set_label('Demand (GWh)')

    # Format the color bar labels as integers with thousands separators
    formatter = ticker.FuncFormatter(lambda x, pos: '{:,.0f}'.format(x))
    cbar.set_ticks(cbar.get_ticks())
    cbar.ax.yaxis.set_major_formatter(formatter)

    # Show the plot
    plt.show()
    
#-------------------------------------------

def analyze_nan_values(df):
    """
    Analyzes and prints information about NaN values in a DataFrame.
    Example usage
    analyze_nan_values(unit_hourly_revenue_df)
    :param df: A Pandas DataFrame.
    """
    
    print(type(df)) 
    
    # Find rows with NaN values
    rows_with_nan = df[df.isna().any(axis=1)]
    
    # Print rows with NaN values
    if not rows_with_nan.empty:
        print("Rows with NaN values:")
        print(rows_with_nan)
        
        # Identify specific columns with NaN values
        for index, row in rows_with_nan.iterrows():
            nan_columns = row[row.isna()].index.tolist()
            print(f"Row {index} has NaN in columns: {nan_columns}")
    else:
        print("No rows with NaN values.")

    # Count of NaN values in each column
    nan_count_per_column = df.isna().sum()
    print("\nNaN count per column:")
    print(nan_count_per_column)

    # Total count of NaN values
    total_nan_count = df.isna().sum().sum()
    print(f"\nTotal number of NaN values in the DataFrame: {total_nan_count}")

#-------------------------------------------

def concatenate_with_year_column(dataframes_by_year, granularity):
    """
    Concatenate dataframes with a 'Year' column from a copy of the input dictionary.

    Args:
    dataframes_by_year (dict): Dictionary of DataFrames keyed by year.
    granularity (str): The time granularity of the data (e.g., 'hourly', 'monthly', etc.).

    Returns:
    pd.DataFrame: Concatenated DataFrame with a 'Year' column.
    """
    concatenated_df = pd.DataFrame()
    copied_dataframes = copy.deepcopy(dataframes_by_year)

    for year, df in copied_dataframes.items():
        # Add a 'Year' column to each DataFrame
        df['Year'] = year
        # Add a 'Granularity' column to identify the granularity of each row
        df['Granularity'] = granularity
        # Concatenate the DataFrame
        concatenated_df = pd.concat([concatenated_df, df])

    return concatenated_df
#-------------------------------------------

def concatenate_annual_dataframes_with_year(dataframes_by_year):
    """
    Concatenate annual DataFrames and include the year as a column.

    Args:
    dataframes_by_year (dict): Dictionary of annual DataFrames keyed by year.

    Returns:
    pd.DataFrame: Concatenated DataFrame of annual data with the year included.
    """
    concatenated_df = pd.DataFrame()

    for year, df in dataframes_by_year.items():
        # Extract year from the index and create a 'Year' column
        df['Year'] = year
        concatenated_df = pd.concat([concatenated_df, df])

    return concatenated_df

#-------------------------------------------
def aggregate_to_frequency(dataframes_by_year, frequency):
    """
    Aggregate data to a specified frequency (monthly or quarterly).

    Args:
    dataframes_by_year (dict): Dictionary of DataFrames keyed by year.
    frequency (str): Frequency for resampling ('M' for monthly, 'Q' for quarterly).

    Returns:
    pd.DataFrame: Aggregated DataFrame.
    """
    aggregated_df = pd.DataFrame()

    for df in dataframes_by_year.values():
        # Resample and sum the data for each period
        resampled_df = df.resample(frequency).sum()
        aggregated_df = pd.concat([aggregated_df, resampled_df])

    return aggregated_df

#-------------------------------------------
def write_df_to_csv_with_progress(df, file_path, chunk_size=10000):
    """
    Writes a DataFrame to a CSV file in chunks with a progress bar.

    :param df: pandas DataFrame to be written to CSV.
    :param file_path: Path of the CSV file to write.
    :param chunk_size: Number of rows per chunk. Default is 10,000.
    """
    number_of_chunks = len(df) // chunk_size + 1

    # Initialize a progress bar
    with tqdm(total=number_of_chunks) as pbar:
        for i in range(number_of_chunks):
            start_idx = i * chunk_size
            end_idx = start_idx + chunk_size
            # Extract chunk of data
            chunk = df.iloc[start_idx:end_idx]
            # Write chunk to file
            mode = 'a' if i > 0 else 'w'  # Append if not the first chunk
            header = i == 0  # Include header only for the first chunk
            chunk.to_csv(file_path, mode=mode, header=header, index=True)
            # Update the progress bar
            pbar.update(1)
#-------------------------------------------
def format_with_commas(x):
    """
    Helper function to format a number with commas.
    """
    try:
        return "{:,.0f}".format(x)  # formats the number with commas and no decimal places
    except:
        return x  # if x is not a number, return as is

#-------------------------------------------
def print_hourly_production_dict_by_asset_summary(hourly_production_dict):
    for year, df in hourly_production_dict.items():

        print(f"Year: {year}")
        print(df.head())  # Prints the first 5 rows of the DataFrame
        print("\n")  # Adds a new line for better readability
    print("Summary printed successfully.")

#-------------------------------------------
def print_annual_production_dict_by_tech_summary(annual_production_by_tech):
    """
    Prints the annual production summary in a table format with numbers formatted with commas.
    
    Parameters:
    annual_production_by_tech (dict): A dictionary where keys are years and values are DataFrames of production data.
    """
    
    # Example usage
    # print_annual_production_summary(annual_production_by_tech)   
    
    dfs = []

    for year, df in annual_production_by_tech.items():
        df_copy = df.copy()
        df_copy['Year'] = year
        df_copy.reset_index(drop=True, inplace=True)
        dfs.append(df_copy)

    annual_summary = pd.concat(dfs)
    annual_summary = annual_summary.set_index('Year').reset_index()

    # Calculate the grand total for each tech type
    annual_summary['Grand Total'] = annual_summary.drop('Year', axis=1).apply(pd.to_numeric, errors='coerce').sum(axis=1)

    # Apply formatting to each column
    annual_summary = annual_summary.map(format_with_commas)

    print(annual_summary.to_string(index=False))

    
#-------------------------------------------
def print_annual_production_dict_by_asset_summary(annual_production_by_asset):
    """
    Prints the annual production summary by asset in a table format with numbers formatted with commas.
    
    Parameters:
    annual_production_by_asset (dict): A dictionary where keys are years and values are DataFrames of production data by asset.
    """
    
    # Example usage
    # print_annual_production_by_asset_summary(annual_production_by_asset)
    
    dfs = []

    for year, df in annual_production_by_asset.items():
        df_copy = df.copy()
        df_copy['Year'] = pd.to_datetime(df_copy.index).year[0]  # Assuming the index is a datetime and all dates within a DataFrame are within the same year
        df_copy.reset_index(drop=True, inplace=True)
        dfs.append(df_copy)

    annual_summary = pd.concat(dfs)
    annual_summary.set_index('Year', inplace=True)

    # Calculate the grand total for each asset
    annual_summary['Grand Total'] = annual_summary.apply(pd.to_numeric, errors='coerce').sum(axis=1)

    # Apply formatting to each column
    annual_summary = annual_summary.map(lambda x: "{:,}".format(x) if isinstance(x, (int, float)) else x)

    print(annual_summary.to_string(index=True))

#-------------------------------------------
# Modified function to create file paths
def create_file_path(base_directory, filename):
    # Determine folder based on file extension
    if filename.endswith('.csv'):
        folder = init.gbl_csv_folder
    elif filename.endswith('.png'):
        folder = init.gbl_image_folder
    else:
        folder = ''  # Default folder if extension is not recognized

    full_path = os.path.join(base_directory, folder, filename)

    # Create folder if it doesn't exist
    if not os.path.exists(os.path.dirname(full_path)):
        os.makedirs(os.path.dirname(full_path))
    
    return full_path

#-------------------------------------------
# Modified function to save figures
def save_figure(figure, filename, dpi=300):
    output_path = create_file_path(init.gbl_base_output_directory_global , filename)
    figure.savefig(output_path, dpi=dpi)
    plt.close(figure)  # Close the figure to free up memory
    
    
# Example usage
# Save as CSV
# filename_csv = 'example.csv'
# full_file_path_csv = create_file_path(init.gbl_base_output_directory_global , filename_csv)
# # Your DataFrame to_csv call here, e.g.,
# # df.to_csv(full_file_path_csv, index=True)

# # Export Image
# filename_img = 'example_plot.png'
# save_figure(plt.gcf(), filename_img)  # Assuming 'plt.gcf()' gets the current figure

# Alternative function to save figures
# Create a figure and axes object
#fig, ax = plt.subplots()
# Plot your data
#ax.plot([1, 2, 3], [4, 5, 6])
#dpi_value = 300  # Example value, adjust as needed
#fig.savefig('my_plot.png', dpi=dpi_value)

#-------------------------------------------
# Saving Plotly Images
def save_plotly_figure(figure, filename, width=1000, height=600, scale=2):
    output_path = create_file_path(init.gbl_base_output_directory_global , filename)
    figure.write_image(output_path, width=width, height=height, scale=scale)


#-------------------------------------------
def prepare_dataframe(df, add_year=True):      
    if 'DateTime' in df.columns:
        df['DateTime'] = pd.to_datetime(df['DateTime'])
        df.set_index('DateTime', inplace=True)

        if add_year and isinstance(df.index, pd.DatetimeIndex):
            df['Year'] = df.index.year

    return df
        
#-------------------------------------------
def prepare_dataframe1(df):
    global glb_date_time_col_name_global
    
    # Check if 'DateTime' is a column, and if so, convert it to datetime format and set as index
    if glb_date_time_col_name_global in df.columns:
        df[glb_date_time_col_name_global] = pd.to_datetime(df[glb_date_time_col_name_global], format=glb_date_time_col_name_global, errors='coerce')
        df.set_index(glb_date_time_col_name_global, inplace=True)

    # Optionally, convert DateTime index to just the year
    # Remove or comment out this part if you want to keep the full datetime information
    if not pd.api.types.is_integer_dtype(df.index):
        df.index = df.index.year

    return df

#-------------------------------------------
def prepare_dataframe2(df):
    if isinstance(df, pd.Series):
        df = df.to_frame()

    if 'DateTime' in df.columns:
        df['DateTime'] = pd.to_datetime(df['DateTime'])
        df.set_index('DateTime', inplace=True)

    if not pd.api.types.is_integer_dtype(df.index):
        df.index = df.index.year  # Ensure index is year as integer

    return df

#-------------------------------------------
def prepare_dataframe_monthly(df):
    # Convert to DataFrame if it's a Series
    if isinstance(df, pd.Series):
        df = df.to_frame()

    # Convert 'DateTime' column to DateTime index if it exists
    if 'DateTime' in df.columns:
        df['DateTime'] = pd.to_datetime(df['DateTime'])
        df.set_index('DateTime', inplace=True)

    # If index is DatetimeIndex, convert to PeriodIndex with monthly frequency
    if isinstance(df.index, pd.DatetimeIndex):
        df.index = df.index.to_period('M')

    return df

#-------------------------------------------
def filter_by_year_and_status(year, status):
    # Convert the year to string because DataFrame column names are strings
    year_str = str(year)
    
    # Merging the yearly status information with the original metadata
    combined_df = gv.metadata.merge(status, on='ASSET_ID', how='left')
    
    # Filter for assets that match the given status for the specified year
    filtered_df = combined_df[combined_df[year_str] == status]
    
    return filtered_df

#-------------------------------------------
def find_missing_hours(data_frames_dict):
    global gbl_start_date, gbl_end_date
    
    # Create a union of all indices from the data frames
    all_indices = None
    for df in data_frames_dict.values():
        if all_indices is None:
            all_indices = df.index
        else:
            all_indices = all_indices.union(df.index)

    missing_hours = {}
    # Find missing date-times in each data frame
    for name, df in data_frames_dict.items():
        # Generate the full range of date-times for the period in the data frame
        start_date = df.index.min()
        end_date = df.index.max()
        full_range = pd.date_range(start=start_date, end=end_date, freq='h')

        # Find missing date-times
        missing_date_times = full_range.difference(df.index)

        # Exclude DST start and end hours for each year
        years = missing_date_times.year.unique()
        
        for year in years:
            # DST rules changed in 2006
            if year >= 2006:
                # DST Start (Second Sunday in March)
                dst_start = pd.Timestamp(f"{year}-03-01") + pd.DateOffset(weeks=1, weekday=6)

                # DST End (First Sunday in November)
                dst_end = pd.Timestamp(f"{year}-11-01") + pd.DateOffset(weekday=6)
                
            else:
                # DST Start (First Sunday in April)
                dst_start = pd.Timestamp(f"{year}-04-01") + pd.DateOffset(weekday=6)

                # DST End (Last Sunday in October)
                dst_end = pd.Timestamp(f"{year}-10-31") - pd.DateOffset(days=(pd.Timestamp(f"{year}-10-31").weekday() + 1) % 7)

            missing_hours[name] = missing_date_times

    return missing_hours

import os

#-------------------------------------------
def reorder_dataframe_columns(df, desired_order):
    """
    Reorders the columns of a DataFrame based on a specified order.

    Parameters:
    df (pandas.DataFrame): The DataFrame to be reordered.
    desired_order (list): A list of column names in the desired order.

    Returns:
    pandas.DataFrame: A DataFrame with columns reordered.
    """
    
    # Usage example:
    # concatenated_hourly_production_by_tech_by_year_df = reorder_dataframe_columns(concatenated_hourly_production_by_tech_by_year_df, tech_type_desired_order)
    
    # Filter out any columns from desired_order that are not in the DataFrame
    ordered_columns = [col for col in desired_order if col in df.columns]

    # Reorder the DataFrame using the filtered list of columns
    return df[ordered_columns]



#-------------------------------------------
def save_df_to_csv(dataframe_dict, base_directory, file_prefix, include_index=False):
    """
    Save each DataFrame in a dictionary to a separate CSV file.

    :param dataframe_dict: Dictionary of DataFrames to be saved.
    :param base_directory: The base directory where the files will be saved.
    :param file_prefix: Prefix for the filename.
    :param include_index: Whether to include the DataFrame index in the CSV. Default is False.
    """
    for key, df in dataframe_dict.items():
        filename_csv = f"{file_prefix}_{key}.csv"
        full_file_path_csv = os.path.join(base_directory, filename_csv)
        df.to_csv(full_file_path_csv, index=include_index)
        print(f"File saved: {full_file_path_csv}")
#-------------------------------------------   
def preprocess_data_frames(data_frames_dict, datetime_col='DateTime'):
    """
    Preprocess the provided data frames for analysis.
    """
    #.......................................................
    def standardize_index(df):
        """
        Check if the data frame has a 'DateTime' column. If so, convert it to datetime and set it as the index.
        If the index is already a datetime, leave it as is.
        """
        if datetime_col in df.columns:
            df[datetime_col] = pd.to_datetime(df[datetime_col], errors='coerce')
            df.set_index(datetime_col, inplace=True)
        elif not pd.api.types.is_datetime64_any_dtype(df.index):
            df.index = pd.to_datetime(df.index, errors='coerce')
        return df

    #.......................................................
    def handle_dst_and_missing_data(data_frames_dict):
        """
        Adjust for DST and fill in missing data.
        """
        updated_dataframes = {}
        duplicate_info = {}  # Container to hold duplicate information for each DataFrame

        # Find missing hours for all data frames
        missing_hours = find_missing_hours(data_frames_dict)
        #print(f"Missing Hour Before Non-DST Hours Removed: {missing_hours}")

        for name, df in data_frames_dict.items():
            #print-out index of each dataframe
            print(f"Within handle_dst_and_missing_data - {name} index.dtype: {df.index.dtype}")
            try:
                modified_df = df.copy()

                # Remove all duplicates
                modified_df = modified_df[~modified_df.index.duplicated(keep='first')]
                print("Duplicates removed")

                # Handle missing hours
                for missing_hour in missing_hours[name]:
                    previous_hour = missing_hour - pd.Timedelta(hours=1)
                    if previous_hour in modified_df.index:
                        # Copy data from the previous hour
                        previous_hour_data = modified_df.loc[previous_hour]
                        # Insert the missing hour with the copied data
                        modified_df.loc[missing_hour] = previous_hour_data
                    else:
                        # Handle case where previous hour is also missing if needed
                        pass

                # Ensure the DataFrame is sorted by index after inserting rows
                modified_df.sort_index(inplace=True)
                print("Sorting data")
                print(modified_df.columns)
                print(f" modified_df:{modified_df.head()}")

                # Forward-fill any remaining gaps
                modified_df = modified_df.asfreq('h', method='ffill')
                print("Forward-fill completed")

                updated_dataframes[name] = modified_df
                print(f"Data frame {name} processed successfully")

                #Check for duplicates during processing
                duplicates = modified_df[modified_df.index.duplicated(keep=False)]
                print(f"Checking duplicates in {name}: {duplicates.empty}")  # Add this line
                if not duplicates.empty:
                    duplicate_info[name] = duplicates
            except Exception as e:
                print(f"An error occurred with DataFrame: {name}")
                print(f"Error: {e}")
                # Break out of the loop upon encountering an error
                #break
        #Check for missing hours again
        missing_hours = find_missing_hours(updated_dataframes)
        #print(f" Missing Hour Check at the end of handle_dst_and_missing_data() = {missing_hours}")
        
        #Print out the duplicate information or confirmation of no duplicates
#         for name in updated_dataframes:
#             if name in duplicate_info:
#                 print(f"Duplicate Hour Check for {name} at the end of handle_dst_and_missing_data():")
#                 print(duplicate_info[name])
#             else:
#                 print(f"No duplicates found in {name} after processing.")
#         print("*" * 90)
        
        return updated_dataframes, duplicate_info, missing_hours
    #.......................................................
    def align_data_frames(data_frames_dict):
        """
        Align all data frames to the date range of the data frame with the shortest end date.
        """
        # Find the earliest maximum (end) date among all data frames
        max_end_date = min(df.index.max() for df in data_frames_dict.values())

        aligned_data_frames_dict = {}
        for name, df in data_frames_dict.items():
            # Align each data frame to the earliest maximum (end) date
            aligned_df = df.loc[:max_end_date]
            aligned_data_frames_dict[name] = aligned_df

        return aligned_data_frames_dict

    #.......................................................
    def check_missing_indices(data_frames):
        """
        Check for missing indices between pairs of data frames.
        """
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
    #.......................................................
    def identify_and_print_duplicates(data_frames_dict):
        """
        Identify and print duplicates in each data frame.
        """
        for name, df in data_frames_dict.items():
            if df.index.duplicated().any():
                duplicates = df[df.index.duplicated(keep=False)]
                print(f" Found duplicates in {name} based on index:")
                print(duplicates)
            else:
                print(f" No duplicates in {name} based on index:")
                print("*" *90)

    #.......................................................
    def check_24_hour_intervals(data_frames_dict):
        """
        Check each data frame for 24-hour intervals on each day and print total missing hours.
        """
        for name, df in data_frames_dict.items():
            # Group by date and count the number of records for each day
            daily_counts = df.groupby(df.index.date).count()

            # Assuming you want to count rows, you can sum across all columns
            row_counts = daily_counts.sum(axis=1)

            # Find days with counts different from 24
            days_with_incorrect_counts = row_counts[row_counts != 24]

            # Calculate the total number of missing hours
            total_missing_hours = sum(24 - count for count in days_with_incorrect_counts)

            print(f"Total missing hours in {name}: {total_missing_hours}")
            print("*" *90)
    #.......................................................
    def process_each_data_frame(data_frames_dict):
        """
        Process each data frame in the dictionary.
        """
        updated_dataframes = {}
        
        #Step 2a:  First, handle DST and missing data for all data frames
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
        
         # Then, apply further processing to each data frame individually
        #for name, df in data_frames_dict.items():
        for name, df in updated_dataframes.items():
            try:
                print(f" Checking {name} for missing date-times:")
                df_copy = df.copy()
                 #Step 2b:
                print(f" Starting Step 2b for {name}")
                df_copy = standardize_index(df_copy)
                print(f" Completed Step 2b: {name} has been processed for standardized index")
                # Further custom processing for each data frame...
                #Step 2c:
                print(f" Starting Step 2c for {name}")
                updated_dataframes[name] = df_copy
                print(f" Completed Step 2c: {name} returned to proceed to Step 3")
                print("*" *90)
            except Exception as e:
                print(f"An error occurred with DataFrame: {name}")
                print(f"Error: {e}")
                break
                
        return updated_dataframes

#-------------------------------------------
    
    # Step 1: Initial Check for Missing Indices
    # This should be done on the original, unprocessed data frames
    print("Starting Step 1")
    missing_indices_info_before = check_missing_indices(list(data_frames_dict.values()))
    for key, value in missing_indices_info_before.items():
        print(f"Initial missing indices between {key[0]} and {key[1]}:", value)
    print("Completed Step 1: Each data frame has been processed for missing indices.")
    print("*" *90)

    # Step 2: Process Each Data Frame
    print("Starting Step 2")
    processed_data_frames_dict = process_each_data_frame(data_frames_dict)
    #print("Completed Step 2: Each data frame has been processed.")

    # Step 2.5: Identifying Duplicates
    print("Starting Step 2.5")
    identify_and_print_duplicates(processed_data_frames_dict)
    print("Completed Step 2.5: Each data frame has been checked again for duplicates.")

    # Step 3: Aligning Data Frames
    print("Starting Step 3")
    aligned_data_frames_dict = align_data_frames(processed_data_frames_dict)
    print("Completed Step 3: Each data frame has been processed for alignement.")

    # Step 4: Identifying Duplicates
    print("Starting Step 4")
    identify_and_print_duplicates(aligned_data_frames_dict)
    print("Completed Step 4: Each data frame has been checked again for duplicates.")

    # Step 5: Check each data frame for 24-hour intervals
    print("Starting Step 5")
    check_24_hour_intervals(aligned_data_frames_dict)
    print("Completed Step 5: Each data frame has been checked to ensure each day as a 24 hour interval.")

    # Step 6: Final Check for Missing Indices
    # This should be done on the processed and aligned data frames
    print("Starting Step 6")
    missing_indices_info_after = check_missing_indices(list(aligned_data_frames_dict.values()))
    for key, value in missing_indices_info_after.items():
        print(f"Final missing indices between {key[0]} and {key[1]}:", value)
    print("Completed Step 6: Each data frame has been checked for missing indices.")
    print("*" *90)
 
        
    return aligned_data_frames_dict

code_end()


############################################

############################################

############################################

############################################