import pandas as pd
import traceback
import datetime
from IPython.display import display
import numpy as np
from tqdm import tqdm

from Utilities import (
    read_from_csv_input_folder,
    save_dataframe_to_csv,
    preprocess_data_frames,
    print_annual_production_dict_by_tech_summary,
    concatenate_with_year_column,
    reorder_dataframe_columns,
    aggregate_to_frequency,
    concatenate_annual_dataframes_with_year
    
)
    
from config import (
    code_begin, 
    code_end, 
    tech_type_desired_order
)

import global_variables as gv # this is an alias for global_variables
import initializer as init
from global_variables import (
    gbl_datetime_hourly_timeseries_format,
    gbl_datetime_col_name, ###############
    gbl_datetime_hourly_timeseries_format,
    gbl_first_year_data,
    gbl_last_year_data,
    gbl_datetime_col_name,
   
    #Meta Data
    gbl_metadata_asset_id_column_hdr,
    gbl_metadata_tech_type_column_hdr,
    gbl_metadata_start_year_column_hdr,
    gbl_metadata_retirement_year_column_hdr,
    gbl_metadata_start_date_column_hdr,
    gbl_metadata_retirement_date_column_hdr,
    gbl_metadata_retirement_year_column_hdr,
    gbl_metadata_status_column_hdr,
    gbl_metadata_development_status_label,
    gbl_metadata_operating_repowered_status_label,
    gbl_metadata_retired_status_label,
    
    #Production Data
    gbl_dateMST_label_existing_production,
    gbl_dateMST_label_update_to_production,
    gbl_up_to_date_production_existing_date_format,
    
    #Spot Power
    gbl_pool_price_template_file,
    glb_pool_price_sub_folder,
    gbl_dateMPT_label_pool_price,
    gbl_pool_price_existing_date_format,
    
    #Nat Gas
    gbl_dateMPT_label_natural_gas,
    
    #Demand
    gbl_demand_template_file,
    gbl_demand_sub_folder,
    gbl_demand_existing_date_format,
    gbl_dateMPT_label_ail_demand,#######
    gbl_dateMPT_label_natural_gas,
    
    gbl_net_export_label,
    gbl_tie_line_label,
    gbl_import_bc_label,
    gbl_import_mt_label,
    gbl_import_sk_label,
    gbl_export_bc_label,
    gbl_export_mt_label,
    gbl_export_sk_label,
    gbl_export_imports_category_list,
)



###################################################
# Metered Volumed Data
###################################################
def run_update_metered_volume():
    global gbl_datetime_col_name
    #global gbl_ide_option
    global gbl_metadata_start_year_column_hdr
    global gbl_metadata_retirement_date_column_hdr
    global gbl_dateMST_label_existing_production
    global gbl_dateMST_label_update_to_production
    global gbl_metadata_retirement_year_column_hdr
    global gbl_metadata_development_status_label
    global gbl_metadata_operating_repowered_status_label
    global gbl_up_to_date_production_data
  

    

    code_begin()

    # Debugging
    print("Debugging - gv.gbl_existing_production_df:", gv.gbl_existing_production_df)
    print("Debugging - gv.gbl_update_to_production_df:", gv.gbl_update_to_production_df)

    #...............................................................................
    #Load Time Series files that are already conslidated into 1 file
    #...............................................................................
    # Step 1: Load files
    #
    #...............................................................................
    #Clean-up Headers and Prepocess Data
    #...............................................................................
    # Print column names to debug
    # print(f" metadata:, {metadata.head()}")
    # print(f" metadata columns: {metadata['ASSET_ID']}")
    
    #global gv.gbl_existing_production_df
    #global gv.gbl_update_to_production_df

    print("existing_production_df columns before renaming:", gv.gbl_existing_production_df.columns)
    print("Update file columns before renaming:", gv.gbl_update_to_production_df.columns)


    # Fix names of columns:
    gv.gbl_existing_production_df.rename(columns={gbl_dateMST_label_existing_production: gbl_datetime_col_name}, inplace=True)
    print(gbl_dateMST_label_existing_production)
    print(gbl_datetime_col_name)
    
    gv.gbl_update_to_production_df.rename(columns={gbl_dateMST_label_update_to_production: gbl_datetime_col_name}, inplace=True)

    # Verify renaming was successful
    if gbl_datetime_col_name not in gv.gbl_existing_production_df.columns:
        raise KeyError(f"Column '{gbl_datetime_col_name}' not found in existing_production_df after renaming.")

    if gbl_datetime_col_name not in gv.gbl_update_to_production_df.columns:
        raise KeyError(f"Column '{gbl_datetime_col_name}' not found in update_to_production_df after renaming.")

    # Step 2: Identify Missing and New Asset IDs
    missing_assets = set(gv.gbl_existing_production_df.columns) - set(gv.gbl_update_to_production_df.columns)
    #Note the Meta Data File has to be aligned with the new update_to_production_df asset columns
    new_assets = set(gv.gbl_update_to_production_df.columns) - set(gv.gbl_existing_production_df.columns)

    # print("Asset IDs Removed in Existing Production Data due to Retirements:", missing_assets)
    # print(f" Total Number of Retired Assets: {len(missing_assets)}")
    # print("*" *90)   
    # print("New Asset IDs in Updated Production Data due to New Supply Coming On-line:", new_assets)
    # print(f" Total Number of New Assets: {len(new_assets)}")
    # print("*" *90)   

    # Add new columns from update_df to base_df
    for column in new_assets:
        gv.gbl_existing_production_df[column] = pd.NA
    #__________________________________________________________________
    # Step 3: Align Date-Time Series and Handle Overlap
    gv.gbl_existing_production_df[gbl_datetime_col_name] = pd.to_datetime(gv.gbl_existing_production_df[gbl_datetime_col_name],errors='coerce')
    print(f" existing_production_df[gbl_datetime_col_name].max: {gv.gbl_existing_production_df[gbl_datetime_col_name].max()}")

    print(f" existing_production_df.columns(): {gv.gbl_existing_production_df.columns}")
    print(f" update_to_production_df.columns(): {gv.gbl_update_to_production_df.columns}")

    # Ensure gbl_datetime_col_name in update DataFrame is  gbl_datetime_col_name format
    gv.gbl_update_to_production_df[gbl_datetime_col_name] = pd.to_datetime(gv.gbl_update_to_production_df[gbl_datetime_col_name],errors='coerce')
    print(f" update_to_production_df[gbl_datetime_col_name].max: {gv.gbl_update_to_production_df[gbl_datetime_col_name].max()}")
    na_rows = gv.gbl_update_to_production_df[gv.gbl_update_to_production_df[gbl_datetime_col_name].isna()]
    print(f" na_rows.index: {na_rows.index}")

    # Find the last date-time in the base_df
    last_base_datetime = gv.gbl_existing_production_df[gbl_datetime_col_name].max()
    print(f" last_base_datetime: {last_base_datetime}")

    # Filter update_df to start 1 hour after last_base_datetime
    overlap_start_time = last_base_datetime + pd.Timedelta(hours=1)
    if pd.isna(overlap_start_time):
        print("Overlap start time is NaT")
    else:
        overlap_df = gv.gbl_update_to_production_df[gv.gbl_update_to_production_df[gbl_datetime_col_name] <= overlap_start_time]
        na_rows = overlap_df[overlap_df[gbl_datetime_col_name].isna()]
        print(f" overlap_df[overlap_df[gbl_datetime_col_name]. na_rows.index: {na_rows.index}")
        print("Ignoring rows from update file up to:", overlap_df[gbl_datetime_col_name].max())
        gv.gbl_update_to_production_df = gv.gbl_update_to_production_df[gv.gbl_update_to_production_df[gbl_datetime_col_name] > overlap_start_time]

    na_rows = gv.gbl_update_to_production_df[gv.gbl_update_to_production_df[gbl_datetime_col_name].isna()]
    print(f" update_to_production_df[update_to_production_df[gbl_datetime_col_name] na_rows.index: {na_rows.index}")

    overlap_df = gv.gbl_update_to_production_df[gv.gbl_update_to_production_df[gbl_datetime_col_name] <= last_base_datetime + pd.Timedelta(hours=1)]


    print(f" overlap_df[gbl_datetime_col_name].max: {overlap_df[gbl_datetime_col_name].max()}")
    na_rows = overlap_df[overlap_df[gbl_datetime_col_name].isna()]
    print(f" na_rows.index: {na_rows.index}")

    gv.gbl_update_to_production_df = gv.gbl_update_to_production_df[gv.gbl_update_to_production_df[gbl_datetime_col_name] > last_base_datetime + pd.Timedelta(hours=1)]

    print("Ignoring rows from update file up to:", overlap_df[gbl_datetime_col_name].max())

    # Step 4: Concatenate the Files
    gbl_up_to_date_production_data = pd.concat([gv.gbl_existing_production_df, gv.gbl_update_to_production_df], ignore_index=True)
    save_dataframe_to_csv(gbl_up_to_date_production_data,'up_to_date_production_data.csv')

    #...............................................................................
    # Read the CSV file into a pandas data frame
    #up_to_date_production_data = pd.read_csv('C:/Users/kaczanor/OneDrive - Enbridge Inc/Documents/Python/AB Electricity Sector Stats/output_data/CSV_Folder/up_to_date_production_data.csv')

    #new
    # Ensure gbl_datetime_col_name in read DataFrame is  gbl_datetime_col_name
    gbl_up_to_date_production_data[gbl_datetime_col_name] = pd.to_datetime(gbl_up_to_date_production_data[gbl_datetime_col_name], errors='coerce')
    print(f" Reloaded up_to_date_production_data.head(): {gbl_up_to_date_production_data.head()}")

    # Check for NaT values in the  gbl_datetime_col_name column
    na_rows = gbl_up_to_date_production_data[gbl_up_to_date_production_data[gbl_datetime_col_name].isna()]
    print(f" Uploaded File na_rows.index: {na_rows.index}")
    ###...............................................................................

    gbl_up_to_date_production_data_asset_ids = gbl_up_to_date_production_data.columns.tolist()
    # List of columns to be removed
    columns_to_remove = {gbl_dateMST_label_update_to_production, gbl_datetime_col_name}


    # Using list comprehension to exclude specified columns and preserve order
    gbl_up_to_date_production_data_asset_ids = [col for col in gbl_up_to_date_production_data_asset_ids if col not in columns_to_remove]
    #print(f" gv.gbl_up_to_date_production_data_asset_ids: {gv.gbl_up_to_date_production_data_asset_ids}")
    #print("*" *90)   

    print(f" up_to_date_production_data.columns: {gbl_up_to_date_production_data.columns}")

    # Step 5: Check for Missing Date-Time Rows

    year_range = range(gbl_up_to_date_production_data[gbl_datetime_col_name].dt.year.min(), gbl_up_to_date_production_data[gbl_datetime_col_name].dt.year.max() + 1)
    missing_hours = {}

    for year in year_range:
        start = pd.Timestamp(year, 1, 1)
        end = pd.Timestamp(year + 1, 1, 1) - pd.Timedelta(hours=1)
        all_hours = pd.date_range(start, end, freq='h')
        actual_hours = gbl_up_to_date_production_data[(gbl_up_to_date_production_data[gbl_datetime_col_name] >= start) & (gbl_up_to_date_production_data[gbl_datetime_col_name] <= end)][gbl_datetime_col_name]
        missing_hours[year] = all_hours.difference(actual_hours)

    # Display missing hours for each year
    # for year, missing in missing_hours.items():
    #     print(f"Year {year} has {len(missing)} missing hours")
    # print("*" *90)  
    
    code_end()

    return
###################################################
# Step 1: Generator Meta Data
###################################################
def run_prep_generator_meta_data():
    ###########################################
    #Meta Data
    ###########################################


    global gbl_metadata_start_year_column_hdr
    global gbl_metadata_retirement_year_column_hdr
    global gbl_metadata_start_date_column_hdr
    global gbl_metadata_asset_id_column_hdr
    global gbl_metadata_tech_type_column_hdr
    global gbl_datetime_col_name
    global gbl_metadata_development_status_label
    

    print(f" gbl_metadata_start_year_column_hdr: {gbl_metadata_start_year_column_hdr}")
    non_integer_start_years = gv.gbl_meta_data_df[gv.gbl_meta_data_df[gbl_metadata_start_year_column_hdr].apply(lambda x: not isinstance(x, int) and not pd.isna(x))]

    # Find non-integer entries for 'RETIREMENT_YEAR'
    non_integer_retirement_years = gv.gbl_meta_data_df[gv.gbl_meta_data_df[gbl_metadata_retirement_year_column_hdr].apply(lambda x: not isinstance(x, int) and not pd.isna(x))]

    # Display these entries
    # print('Non-integer Start Years:')
    # print(non_integer_start_years[gbl_metadata_start_year_column_hdr])
    # print('Non-integer Retirement Years:')
    # print(non_integer_gbl_metadata_retirement_year_column_hdrs[gbl_metadata_retirement_year_column_hdr])

    # Replace non-integer gbl_metadata_start_year_column_hdr entries with NaN
    # With this change, the fillna operation assigns the result back to the DataFrame without using inplace=True, 
    # which should be compatible with future versions of pandas and avoid the warning you were seeing.
    gv.gbl_meta_data_df[gbl_metadata_start_year_column_hdr] = pd.to_numeric(gv.gbl_meta_data_df[gbl_metadata_start_year_column_hdr], errors='coerce')

    # Replace non-integer 'RETIREMENT_YEAR' entries with NaN
    gv.gbl_meta_data_df[gbl_metadata_retirement_year_column_hdr] = pd.to_numeric(gv.gbl_meta_data_df[gbl_metadata_retirement_year_column_hdr], errors='coerce')

    # Fill NaNs with a placeholder like 2000 and 2050 (assuming these are valid years in your dataset)
    gv.gbl_meta_data_df[gbl_metadata_start_year_column_hdr] = gv.gbl_meta_data_df[gbl_metadata_start_year_column_hdr].fillna(2000).astype(int)
    gv.gbl_meta_data_df[gbl_metadata_retirement_year_column_hdr] = gv.gbl_meta_data_df[gbl_metadata_retirement_year_column_hdr].fillna(2050).astype(int)

    # Now ensure that the data types are integers
    gv.gbl_meta_data_df[gbl_metadata_start_year_column_hdr] = gv.gbl_meta_data_df[gbl_metadata_start_year_column_hdr].astype(int)
    gv.gbl_meta_data_df[gbl_metadata_retirement_year_column_hdr] = gv.gbl_meta_data_df[gbl_metadata_retirement_year_column_hdr].astype(int)

    #all_asset_id = gv.gbl_meta_data_df['ASSET_ID']
    #Create a list of all ASSET_IDs in the ASESO production files
    #set(up_to_date_production_data.columns): This converts the columns of your DataFrame into a set. 
    #The important thing to note here is that sets in Python are unordered collections. This means that 
    #when you convert a list (or any sequence) to a set, the original ordering is lost. 
    #As a result, metered_production_asset_ids will be an unordered collection of your original column names, minus gbl_datetime_col_name.
    #If you need to preserve the order of the columns while still performing this operation, you can use a list comprehension 
    #or a similar approach that maintains order. For example: metered_production_asset_ids = [col for col in up_to_date_production_data.columns if col != gbl_datetime_col_name]

    # metered_production_asset_ids = set(up_to_date_production_data.columns) - {gbl_datetime_col_name}
    # print(f" Total Number of Assets in ASEO Metered Production Data: {len(metered_production_asset_ids)}")
    # print(f" Total Number of Assets in ASEO Metered Production Data: {metered_production_asset_ids}")

    #Create a list of all ASSET_IDs in the meta data file
    metadata_asset_ids = set(gv.gbl_meta_data_df[gbl_metadata_asset_id_column_hdr])
    #print(f" Total Number of Assets in Meta Data: {len(metadata_asset_ids)}")

    # Note the all_asset_id and metadata_assets would be the same if the metadat perfectly matched 
    # the ASEO production data.  However it depends on how many years of ASEO production data you 
    # have in your input files.  Older ASEO files 2000 to 2009 have ASSET_IDs for units that have since retired.
    # Newer ASESO proudction files 2010-2024 do not inlcude those assets in their data.  So this code
    # is used to make the AESO production data the drive of the ASSET_ID list to avoide any errors due to missing data

    # Create a list of ASSET_IDs that we had to create in the gv.gbl_meta_data_df that differ from the AESO production file.
    # This is related to assets that have been repowered/or refired.  The AESO continues to use the same ASSET_ID
    # for assets like this.  We however want to differentiate the proudction pre and post repowering as some of these
    # units converted from coal to natural gas.Thi affects emisssions an other assumptions


    # Identify rows where ASSET_ID is a float
    float_asset_ids = gv.gbl_meta_data_df[gv.gbl_meta_data_df[gbl_metadata_asset_id_column_hdr].apply(lambda x: isinstance(x, float))]

    # Display these rows
    print(f" float_asset_ids:{float_asset_ids}")

    print(f" gv.gbl_meta_data_df.head:, {gv.gbl_meta_data_df.head()}")
    display(f" ASSET_IDs: {gv.gbl_meta_data_df[gbl_metadata_asset_id_column_hdr]}")

    special_ids_dict = {}

    for asset_id in tqdm(gv.gbl_meta_data_df[gbl_metadata_asset_id_column_hdr]):
        if asset_id.endswith('*'):
            original_id = asset_id.rstrip('*')
            if original_id in gv.gbl_meta_data_df[gbl_metadata_asset_id_column_hdr].values:
                # Assuming you have START_DATE information in your gv.gbl_meta_data_df
                start_date = gv.gbl_meta_data_df.loc[gv.gbl_meta_data_df[gbl_metadata_asset_id_column_hdr] == asset_id, gbl_metadata_start_date_column_hdr].iloc[0]
                special_ids_dict[original_id] = {'revised_id': asset_id, gbl_metadata_start_date_column_hdr: start_date}
    #print("Special Asset IDs for Repowered Assets:", special_ids_dict)
                
 
    # In Meta Data File - Adjust the recalculate_status function to handle NaT values correctly
    def recalculate_status(row, year):
        # Assume a mid-year point by creating a date with year-06-30
        year_date = pd.Timestamp(year=year, month=6, day=30)
        
        # Use pd.isna to check for NaT (missing date) in START_DATE and RETIREMENT_DATE
        start_date = row[gbl_metadata_start_date_column_hdr]
        retirement_date = row[gbl_metadata_retirement_date_column_hdr] if not pd.isna(row[gbl_metadata_retirement_date_column_hdr]) else pd.Timestamp.max

        # Apply the logic described to determine the status
        if pd.isna(start_date) or year_date < start_date:
            return gbl_metadata_development_status_label 
        elif start_date <= year_date < retirement_date:
            return gbl_metadata_operating_repowered_status_label 
        else:
            return gbl_metadata_retired_status_label 

    # Define the range of years we are interested in
    years_range = range(gbl_first_year_data, gbl_last_year_data + 2)   

    # Recheck the data types for START_DATE and RETIREMENT_DATE columns
    gv.gbl_meta_data_df[gbl_metadata_start_date_column_hdr] = pd.to_datetime(gv.gbl_meta_data_df[gbl_metadata_start_date_column_hdr], errors='coerce')
    gv.gbl_meta_data_df[gbl_metadata_retirement_date_column_hdr] = pd.to_datetime(gv.gbl_meta_data_df[gbl_metadata_retirement_date_column_hdr], errors='coerce')
    # print(f" gv.gbl_meta_data_df[tech_type_column_hdr].unique: {gv.gbl_meta_data_df[tech_type_column_hdr].unique}")

    # Verify that the dates are in  gbl_datetime_col_name format now
    date_conversion_check = gv.gbl_meta_data_df[[gbl_metadata_start_date_column_hdr, gbl_metadata_retirement_date_column_hdr]].map(lambda x: isinstance(x, pd.Timestamp))

    # Find if there are any rows that were not converted successfully (i.e., not Timestamps)
    conversion_issues = gv.gbl_meta_data_df[~date_conversion_check.all(axis=1)]

    # If there are any issues, they will be displayed
    conversion_issues[[gbl_metadata_start_date_column_hdr, gbl_metadata_retirement_date_column_hdr]] if not conversion_issues.empty else "All dates converted successfully."

    #Dynmaic STATUS List
    # 1. Create the Status DataFrame for each ASSET_ID across years
    status_over_years = {gbl_metadata_asset_id_column_hdr: gv.gbl_meta_data_df[gbl_metadata_asset_id_column_hdr]}
    for year in years_range:
        status_over_years[str(year)] = gv.gbl_meta_data_df.apply(lambda row: recalculate_status(row, year), axis=1)

    gbl_status_df = pd.DataFrame(status_over_years)
    print(f"gv.gbl_meta_data_df[tech_type_column_hdr].unique(): {gv.gbl_meta_data_df[gbl_metadata_tech_type_column_hdr].unique()}")
    ##############################
    # Filter the 'SOLAR' assets in the gv.gbl_meta_data_df
    solar_assets = gv.gbl_meta_data_df[gv.gbl_meta_data_df[gbl_metadata_tech_type_column_hdr] == 'SOLAR']

    # Apply the recalculate_status function to each 'SOLAR' asset for the year 2023
    solar_statuses = solar_assets.apply(lambda row: recalculate_status(row, 2023), axis=1)

    # Print the unique statuses assigned to 'SOLAR' assets for 2023
    print("Unique statuses for SOLAR assets in 2023:", solar_statuses.unique())

    ###############################
    # 2. & 3. Create the Dictionary of Yearly DataFrames
    yearly_dataframes = {}

    # Adjusting the loop that creates yearly dataframes to avoid STATUS column duplication
    for year in years_range:
        # Extract the dynamically calculated status for the specific year
        dynamic_status = gbl_status_df[[gbl_metadata_asset_id_column_hdr, str(year)]].rename(columns={str(year): 'DYNAMIC_STATUS'})

        # Merge the dynamic status with the gv.gbl_meta_data_df
        year_df = gv.gbl_meta_data_df.merge(dynamic_status, on=gbl_metadata_asset_id_column_hdr)

        # Replace the original STATUS column with the dynamically calculated status
        year_df[gbl_metadata_status_column_hdr] = year_df['DYNAMIC_STATUS']
        year_df.drop('DYNAMIC_STATUS', axis=1, inplace=True)

        # Store the updated DataFrame in the dictionary
        yearly_dataframes[year] = year_df

    # Now 'yearly_dataframes' is a dictionary where each key is a year, and the value is the corresponding DataFrame

    # Example of accessing the DataFrame for a specific year (e.g., 2021)
    #df_2023 = yearly_dataframes[2023]
    #print(f" df_2023.head: {df_2021.head()}")

    # Diagnostic Step: Check for rows with TECH_TYPE 'SOLAR' that also meet the STATUS filter
    status = [gbl_metadata_operating_repowered_status_label]  # Put the status in a list

    # Diagnostic Step: Check for rows with TECH_TYPE 'SOLAR' that also meet the STATUS filter
    # solar_rows = df_2023[(df_2023[tech_type_column_hdr] == 'SOLAR') & (df_2023[STATUS_COLUMN_HDR ].isin(status))]
    # print("Number of SOLAR rows meeting the STATUS filter:", len(solar_rows))

    # Save as CSV
    # filename_csv = 'Updated_production.csv'
    # full_file_path_csv = create_file_path(base_output_directory_global , filename_csv)
    # up_to_date_production_data.to_csv(full_file_path_csv, index=True)

    #save_dataframe_to_csv(init.gbl_ide_option, up_to_date_production_data,'Updated_production')

    code_end()

    return

###################################################
# Step 2: Concatenate and Prep Spot Power Data
###################################################
def run_hourly_spot_power_data_prep():
    # Remember that the pool price data were not uploaded to a df in the run_prep_demand_data function.  All we did was create as a template file. 
    # The actual data is loaded in this function and you do not need to use the alias gbl_demand_data`'gv.gbl_demand_data'
    # unlike the other data sets`
    
    #Load and Combine Individual Annual Hourly Spot Price Data Files and Updated Metered Volume Data
    global gbl_datetime_hourly_timeseries_format
    global gbl_datetime_col_name, gbl_dateMPT_label_pool_price, gbl_pool_price_existing_date_format,glb_pool_price_sub_folder
    global gbl_pool_price_template_file
    global gbl_pool_price_data
    
    try:
        gbl_pool_price_data = []
        print(f" gbl_first_year_data: {gbl_first_year_data}")
        print(f" gbl_last_year_data: {gbl_last_year_data}")


        for year in tqdm(range(gbl_first_year_data, gbl_last_year_data+1)):
            print(year)
            temp_df = read_from_csv_input_folder(f"{gbl_pool_price_template_file}{year}.csv" , glb_pool_price_sub_folder)
            print(f" temp_df: {temp_df}")
            gbl_pool_price_data.append(temp_df)
        gbl_pool_price_data = pd.concat(gbl_pool_price_data, ignore_index=True)
        print(f" gbl_pool_price_data: {gbl_pool_price_data.head()}")
        gbl_pool_price_data.rename(columns={gbl_dateMPT_label_pool_price: gbl_datetime_col_name}, inplace=True)
        print(f" gbl_pool_price_data: {gbl_pool_price_data.head()}")
        
        print(f" gbl_pool_price_data.columns: {gbl_pool_price_data.columns}")
        print(f" gbl_pool_price_data.index.dtype: {gbl_pool_price_data.index.dtype}")
        print(f" gbl_pool_price_data.head(): {gbl_pool_price_data.head()}")
        
        #DateTimne Conversion
        # Ensure the datetime column is in the correct format
        #Step 1: Convert the existing string format to a datetime object
        gbl_pool_price_data[gbl_datetime_col_name] = pd.to_datetime(gbl_pool_price_data[gbl_datetime_col_name], format = gbl_pool_price_existing_date_format)
        # Step 2: Convert the datetime object to the desired string format
        gbl_pool_price_data[gbl_datetime_col_name] = gbl_pool_price_data[gbl_datetime_col_name].dt.strftime(gbl_datetime_hourly_timeseries_format)
        # Step 3: Set index 
        gbl_pool_price_data.set_index(gbl_datetime_col_name, inplace=True, drop=False)
        
        print(f" pool gbl_pool_price_data columns: {gbl_pool_price_data.columns}")
        print(f" gbl_pool_price_data tail: {gbl_pool_price_data.tail()}")
        print(f" gbl_pool_price_data: {gbl_pool_price_data}")
    except Exception as e:
        print(traceback.format_exc())

    return

###################################################
# Step 3: Create and Prep Annual Hourly Natural Gas Data
###################################################

def generate_yearly_timestamps(year, leap_year_check):
    timestamps = pd.DatetimeIndex([])

    # Number of days in each month
    days_in_month = [31, 29 if leap_year_check else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    for month, days in tqdm(enumerate(days_in_month, start=1)):
        start_date = datetime.datetime(year, month, 1)
        end_date = datetime.datetime(year, month, days, 23)
        monthly_timestamps = pd.date_range(start=start_date, end=end_date, freq='H')
        timestamps = timestamps.append(monthly_timestamps)

    # DST adjustments
    # Find the second Sunday in March for the start of DST
    march_sundays = timestamps[(timestamps.month == 3) & (timestamps.dayofweek == 6)]
    dst_start = march_sundays[1] +  datetime.timedelta(hours=2) # 2 AM on the second Sunday in March

    # Find the first Sunday in November for the end of DST
    november_sundays = timestamps[(timestamps.month == 11) & (timestamps.dayofweek == 6)]
    dst_end = november_sundays[0] +  datetime.timedelta(hours=1) # 1 AM on the first Sunday in November

    # Remove the 2 AM hour for the start of DST
    timestamps = timestamps.delete(np.where(timestamps == dst_start)[0][0])

    # Repeat the 1 AM hour for the end of DST
    dst_end_index = np.where(timestamps == dst_end)[0][0]
    timestamps = timestamps.insert(dst_end_index + 1, dst_end)
    
    return timestamps

#Create Natural Gas Annual Data Frame from 2D Table 
# import pandas as pd
# from  gbl_datetime_col_name import  gbl_datetime_col_name, timedelta
# import numpy as np
def is_leap_year(year):
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


def create_annual_dataframes(year, gbl_dateMPT_label_natural_gas):
    #global gbl_daily_nat_gas_prices_df

    # Iterate over each year's column (skipping the 'Days' column)
    #for year in df_prices.columns[1:]:
    # Generate the correct sequence of timestamps for the year
    
    leap_year_check = is_leap_year(year)
    
    timestamps = generate_yearly_timestamps(int(year),leap_year_check)
    
    # Extract the prices for the year, clean them and repeat each price for each hour of the day
    #The str(year) conversion is essential because your DataFrame columns are string representations of the years (like '2010'), not integers.
    year_column = str(year)
    #print(f" Price Column Check: {naturalgasprice_full_data.columns}")
    #print("*" *90)
    
    year_data = gv.gbl_daily_nat_gas_prices_df[year_column]
    prices = year_data.replace('[^\\d.]+', '', regex=True)
  
    
    
    prices = prices.astype(float).repeat(24).tolist()
 
    # Here, insert the logic to handle DST adjustments akin to how the AESO presents this in their hourly time series data 
    # Correct the prices list for the DST changes
    dst_start_date = timestamps[(timestamps.month == 3) & (timestamps.dayofweek == 6)][1] +  datetime.timedelta(hours=2) # Second Sunday of March at 2 AM
    dst_end_date = timestamps[(timestamps.month == 11) & (timestamps.dayofweek == 6)][0] +  datetime.timedelta(hours=1) # First Sunday of November at 1 AM

    # Remove an hour in March (23 hours for that day)
    if dst_start_date in timestamps:
        dst_start_index = np.where(timestamps == dst_start_date)[0][0]
        prices.pop(dst_start_index)

    # Duplicate an hour in November (25 hours for that day)
    if dst_end_date in timestamps:
        dst_end_index = np.where(timestamps == dst_end_date)[0][0]
        prices.insert(dst_end_index, prices[dst_end_index])

    # Adjust prices if there's still a length mismatch
    price_length_difference = len(timestamps) - len(prices)
    if price_length_difference > 0:
        prices.extend([prices[-1]] * price_length_difference)
    elif price_length_difference < 0:
        prices = prices[:price_length_difference]

    # Create a new DataFrame for the new hourly data format created from the annual natural gas data
    hourly_nat_gas_prices = pd.DataFrame({gbl_dateMPT_label_natural_gas: timestamps, 'NAT_GAS_PRICE': prices})
    print(f" hourly_nat_gas_prices.shape: {hourly_nat_gas_prices.shape}")
    
    # Add debugging print statements to check the DataFrame
    # print(f"hourly_nat_gas_prices columns: {hourly_nat_gas_prices.columns}")
    # print(f"Sample data from hourly_nat_gas_prices:\n{hourly_nat_gas_prices.head()}")

    return hourly_nat_gas_prices

# Create separate annual natural gas data frame for current year
# and then apend the files to create one large hourly natural gas files 

def run_prep_natural_gas_data():
    code_begin()
    global gbl_hourly_nat_gas_price_data

    #dateMST_label = 'DATE_BEGIN_LOCAL'
    #datetime_format = '%Y-%m-%d %H:%M'

    #daily_nat_gas_prices = read_from_csv_input_folder(init.gbl_ide_option, 'AECO Natural Gas 2000 to 2023 daily 04012024', 'aeco-daily-natural-gas-prices-2000-to-2024')

    # hourly_nat_gas_prices = []
    # hourly_nat_gas_price_data = []  # This list will store each year's DataFrame

    all_annual_dataframes = []  # This list will store each year's DataFrame

    print("Daily Nat Gas Prices")
    display(gv.gbl_daily_nat_gas_prices_df)
    print(gv.gbl_daily_nat_gas_prices_df.dtypes)
    print(gv.gbl_daily_nat_gas_prices_df.columns)

    try:

        for year in tqdm(range(gbl_first_year_data, gbl_last_year_data + 1)):
            print(f" natgas year loop: {year}")
            # Create an annual hourly data frame for the given year for natural gas prices
            annual_hourly_nat_gas_prices = create_annual_dataframes(year, gbl_dateMPT_label_natural_gas)
            print(f" annual_hourly_nat_gas_prices.head(): {annual_hourly_nat_gas_prices.head()}")
            
            # Convert the date time column to a DateTime type before appending
            annual_hourly_nat_gas_prices[gbl_dateMPT_label_natural_gas] = pd.to_datetime(annual_hourly_nat_gas_prices[gbl_dateMPT_label_natural_gas], format=gbl_datetime_hourly_timeseries_format)
            #append the annual data frame to the list
            all_annual_dataframes.append(annual_hourly_nat_gas_prices)

        # Concatenate individual hourly data frames
        gbl_hourly_nat_gas_price_data = pd.concat(all_annual_dataframes, ignore_index=True)
        print(f" annual_hourly_nat_gas_prices.head(): {gbl_hourly_nat_gas_price_data.head()}")
        
        # Set the DATE_BEGIN_LOCAL column as the index of the DataFrame
        gbl_hourly_nat_gas_price_data.rename(columns={gbl_dateMPT_label_natural_gas: gbl_datetime_col_name}, inplace=True)
        print(f" annual_hourly_nat_gas_prices.head(): {gbl_hourly_nat_gas_price_data.head()}")
        
        
        
        #DateTime Conversion
        # Ensure the datetime column is in the correct format
        #Step 1: Convert the existing string format to a datetime object
        gbl_hourly_nat_gas_price_data[gbl_datetime_col_name] = pd.to_datetime(gbl_hourly_nat_gas_price_data[gbl_datetime_col_name], \
             format = gbl_dateMPT_label_natural_gas)
        print("Step 1: Convert the existing string format to a datetime object")
        print(f" annual_hourly_nat_gas_prices.head(): {gbl_hourly_nat_gas_price_data.head()}")
        
        # Step 2: Convert the datetime object to the desired string format
        gbl_hourly_nat_gas_price_data[gbl_datetime_col_name] = gbl_hourly_nat_gas_price_data[gbl_datetime_col_name].dt.strftime(\
            gbl_datetime_hourly_timeseries_format)
        
        print("Step 2: Convert the datetime object to the desired string format")
        print(f" gbl_hourly_nat_gas_price_data.head(): {gbl_hourly_nat_gas_price_data.head()}")
        
        # Step 3: Set index
        gbl_hourly_nat_gas_price_data.set_index(gbl_datetime_col_name, inplace=False, drop=False)  
        print("Step 3: Set index")
        print(f" gbl_hourly_nat_gas_price_data.head(): {gbl_hourly_nat_gas_price_data.head()}")
        

        print(f" gbl_hourly_nat_gas_price_data['NAT_GAS_PRICE'].head(): {gbl_hourly_nat_gas_price_data['NAT_GAS_PRICE'].head()}")
        print(f" gbl_hourly_nat_gas_price_data['NAT_GAS_PRICE'].tail(): {gbl_hourly_nat_gas_price_data['NAT_GAS_PRICE'].tail()}")
        
        print(f" gbl_hourly_nat_gas_price_data.index.dtype: {gbl_hourly_nat_gas_price_data.index.dtype}")
        print(f" gbl_hourly_nat_gas_price_data.index: {gbl_hourly_nat_gas_price_data.index}")
        
        save_dataframe_to_csv(gbl_hourly_nat_gas_price_data,'hourly_nat_gas_price_data.csv')
        
    except Exception as e:  # Catch a more general exception
        print(f"An error occurred: {e}")

    code_end()
    
    return

#########################################################
# Concatenate and Prep Demand Data
#########################################################
def run_prep_on_demand_data():
    # Remember that the demand data were not uploaded to a df in the run_prep_demand_data function.  All we did was create as a template file. 
    # The actual data is loaded in this function and you do not need to use the alias gbl_demand_data`'gv.gbl_demand_data'
    # unlike the other data sets`
    global gbl_demand_data 
    global gbl_first_year_data
    global gbl_last_year_data
    global gbl_demand_template_file
    global gbl_demand_data
    global gbl_demand_sub_folder
    global gbl_datetime_col_name
    global gbl_dateMPT_label_ail_demand
    global gbl_demand_existing_date_format
    #_____________________________________________________
    # Step: 4 Load and combine annual demand data files
    #_____________________________________________________
    try:
        #Create list to store the annual demand data
        gbl_demand_data = []
        #subfolder_name = "aeso-metered-demand-2000-to-2023"
        #demand_data_template ="Metered_Demand_"
        # Construct the full path

        for year in tqdm(range(gbl_first_year_data, gbl_last_year_data+1)):
            temp_df = read_from_csv_input_folder(f"{gbl_demand_template_file}{year}.csv", gbl_demand_sub_folder)
            print(f" demand year: {year}")
            gbl_demand_data.append(temp_df)
        #print(f" temp_df Columns: {temp_df.columns}")
        #print(f" temp_df: {temp_df}")
        gbl_demand_data = pd.concat(gbl_demand_data, ignore_index=True)
        gbl_demand_data.rename(columns={gbl_dateMPT_label_ail_demand : gbl_datetime_col_name}, inplace=True)
        
        # First check on index type
        print(f" gbl_demand_data.columns: {gbl_demand_data.columns}")
        print(f" gbl_demand_data: {gbl_demand_data}")
        print(f" gbl_demand_data.index.dtype: {gbl_demand_data.index.dtype}")
        print("*" *90) 
        
        # DateTimne Conversion
        # Ensure the datetime column is in the correct format
        #Step 1: Convert the existing string format to a datetime object
        gbl_demand_data[gbl_datetime_col_name] = pd.to_datetime(gbl_demand_data[gbl_datetime_col_name], \
            format = gbl_demand_existing_date_format)
        # Step 2: Convert the datetime object to the desired string format
        gbl_demand_data[gbl_datetime_col_name] = gbl_demand_data[gbl_datetime_col_name].dt.strftime(\
            gbl_datetime_hourly_timeseries_format)
        # Step 3: Set index
        gbl_demand_data.set_index(gbl_datetime_col_name, inplace=True, drop=False)
        
        # Second check on index type
        print(f" gbl_demand_data.columns: {gbl_demand_data.columns}")
        print(f" gbl_demand_data: {gbl_demand_data}")
        print(f" gbl_demand_data.index.dtype: {gbl_demand_data.index.dtype}")
        print("*" *90)   

        #################################################################
        #Clean-up Headers and Prepocess Data
        #################################################################
        # Fill NaN values with 0 in the relevant columns
        gbl_demand_data[gbl_export_imports_category_list] = gbl_demand_data[gbl_export_imports_category_list].fillna(0)

        #may not need this anymore
        # Calculate the net export data and create a new column in the data frame to store that value
        gbl_demand_data['Net_Export'] = (gbl_demand_data[gbl_import_bc_label] + gbl_demand_data[gbl_import_mt_label] + gbl_demand_data[gbl_import_sk_label]) - \
            (gbl_demand_data[gbl_export_bc_label] + gbl_demand_data[gbl_export_mt_label] + gbl_demand_data[gbl_export_sk_label])

    except Exception as e:
        print(traceback.format_exc())
    return

#########################################################
# Production Data
#########################################################
def run_prep_on_production_data():
    global gbl_up_to_date_production_data
    global gbl_up_to_date_production_existing_date_format
    
    # DateTimne Conversion
    # Ensure the datetime column is in the correct format
    #Step 1: Convert the existing string format to a datetime object
    gbl_up_to_date_production_data[gbl_datetime_col_name] = pd.to_datetime(gbl_up_to_date_production_data[gbl_datetime_col_name], \
            format = gbl_up_to_date_production_existing_date_format)
    print(f" gbl_up_to_date_production_data: {gbl_up_to_date_production_data.head()}")
    
    # Step 2: Convert the datetime object to the desired string format
    gbl_up_to_date_production_data[gbl_datetime_col_name] = gbl_up_to_date_production_data[gbl_datetime_col_name].dt.strftime(gbl_datetime_hourly_timeseries_format)
    
    # Step 3: Set index
    gbl_up_to_date_production_data.set_index(gbl_datetime_col_name, inplace=True, drop=False)
    
    
    print(f" gbl_up_to_date_production_data.columns: {gbl_up_to_date_production_data.columns}")
    print(f" gbl_up_to_date_production_data: {gbl_up_to_date_production_data}")
    print(f" gbl_up_to_date_production_data.index: {gbl_up_to_date_production_data.index}")
    print("*" *90) 
    
    return



#########################################################
def run_clean_all_data():
    #Concatenate and Align Data for Cleaning
    code_begin()
    
    #input data
    global gbl_demand_data, gbl_hourly_nat_gas_price_data, gbl_pool_price_data, gbl_up_to_date_production_data, gbl_meta_data
    
    #final processed data
    global gbl_processed_price_data, gbl_processed_nat_gas_price, gbl_processed_production_data , gbl_processed_demand_data 
    # Labels and Formatting
    global gbl_net_export_label
    global gbl_tie_line_label
    global gbl_datetime_col_name, gbl_datetime_hourly_timeseries_format
    
    #################################################################
    # Align All Hourly Data Sets in Preperation for Analysis
    #################################################################
    #print index of each data frame
    print(f" gbl_pool_price_data.index.dtypes: {gbl_pool_price_data.index.dtype}")       
    print(f" up_to_date_production_data.index.dtypes: {gbl_up_to_date_production_data.index.dtype}")  
    print(f" gbl_demand_data.index.dtypes: {gbl_demand_data.index.dtype}")
    print(f" gbl_hourly_nat_gas_price_data.index.dtypes: {gbl_hourly_nat_gas_price_data.index.dtype}")
    print("*" *90)  
    
    #print data types of returned objects
    print(f" gbl_pool_price_data.dtypes: {gbl_pool_price_data.dtypes}")       
    print(f" up_to_date_production_data.dtypes: {gbl_up_to_date_production_data.dtypes}")  
    print(f" gbl_demand_data.dtypes: {gbl_demand_data.dtypes}")
    print(f" gbl_hourly_nat_gas_price_data: {gbl_hourly_nat_gas_price_data.dtypes}")
    print("*" *90)   

    #print data types of returned objects
    print(f" gbl_pool_price_data: {gbl_pool_price_data}")       
    print(f" up_to_date_production_data: {gbl_up_to_date_production_data}")  
    print(f" gbl_demand_data: {gbl_demand_data}")
    print(f" gbl_hourly_nat_gas_price_data: {gbl_hourly_nat_gas_price_data}")
    print("*" *90)   


    #Load data frames into dictionary in order to pass them as a group to the processing function
    data_frames_dict_to_process = {
        'pool_price_data': gbl_pool_price_data, 
        'hourly_nat_gas_price_data' : gbl_hourly_nat_gas_price_data,
        'up_to_date_production_data': gbl_up_to_date_production_data, 
        'demand_data': gbl_demand_data
    }
    # Identify any data frame(s) have the missing date values and either remove them or fill in the missing value
    for name, df in tqdm(data_frames_dict_to_process.items()):
        if df.index.isna().any():  # check for any missing values in the index
            print(f"{name} has missing date values in the index")
            missing_dates = df.index[df.index.isna()]  # get the dates with missing values
            print(f"Missing dates: {missing_dates}")

    # Print the date range of each data frame before processing
    for name, df in data_frames_dict_to_process.items():
        print(f"{name} date range: {df.index.min()} to {df.index.max()}")
    print("*" *90)   

    gbl_processed_data_frames_dict = preprocess_data_frames(data_frames_dict_to_process)

    print(gbl_pool_price_data.info())
    print(gbl_pool_price_data.head())
    #print("Is index sorted:", gbl_pool_price_data.index.is_monotonic)

    print("Is gbl_pool_price_data index sorted in increasing order:", gbl_pool_price_data.index.is_monotonic_increasing)
    print("Is hourly_nat_gas_price_data index sorted in increasing order:", gbl_hourly_nat_gas_price_data.index.is_monotonic_increasing)
    print("Is up_to_date_production_data index sorted in increasing order:", gbl_up_to_date_production_data.index.is_monotonic_increasing)
    print("Is demand_data index sorted in increasing order:", gv.gbl_demand_data.index.is_monotonic_increasing)

    print(f" data_frames_dict_to_process.keys): {data_frames_dict_to_process.keys}")

    # Accessing the processed data dictionaries
    gbl_processed_price_data = gbl_processed_data_frames_dict['gbl_pool_price_data']
    gbl_processed_nat_gas_price = gbl_processed_data_frames_dict['hourly_nat_gas_price_data']
    gbl_processed_production_data = gbl_processed_data_frames_dict['up_to_date_production_data']
    gbl_processed_demand_data = gbl_processed_data_frames_dict['demand_data']

    if gbl_processed_production_data.index.duplicated().any():
        print("At Time of Function Exit: Duplicates found in processed_production_data")
    else:
        print("At Time of Function Exit: No duplicates found in processed_production_data")

    ########################################
    #print data types of returned objects
    print(f" processed_demand_data.dtypes: {gbl_processed_demand_data.dtypes}")       
    print(f" processed_production_data.dtypes: {gbl_processed_production_data.dtypes}")  
    print(f" processed_price_data.dtypes: {gbl_processed_price_data.dtypes}")       
    print("*" *90)   

    # Print the aligned date range for each processed data frame
    print("Aligned Date Range for Each Processed Data Frame:")
    for name, df in tqdm(gbl_processed_data_frames_dict.items()):
        aligned_min_date = df.index.min()
        aligned_max_date = df.index.max()
        print(f"{name}: {aligned_min_date} to {aligned_max_date}")

    print("*" *90)
    print("Sample data before conversion:")
    print(f" processed_demand_data: {gbl_processed_demand_data}")       
    print(f" processed_demand_data: {gbl_processed_production_data}")   
    print(f" processed_price_data: {gbl_processed_price_data}")       

    print("processed_demand_data name:", gbl_processed_demand_data)
    print("processed_production_data name:", gbl_processed_production_data)
    print("processed_price_data name:", gbl_processed_price_data)
    print("*" *90)   

    print(gbl_processed_demand_data.columns)       
    print(gbl_processed_production_data.columns)   
    print(gbl_processed_price_data.columns)       

    print("processed_demand_data:", gbl_processed_demand_data.index[:5])       # Display first 5  gbl_datetime_col_name indices from demand data
    print("processed_production_data:", gbl_processed_production_data.index[:5])   # Display first 5  gbl_datetime_col_name indices from production data
    print("processed_price_data:" ,gbl_processed_price_data.index[:5])        # Display first 5  gbl_datetime_col_name indices from price data
    print("*" *90)   


    #################################################################
    #Transfer Data Between Data Sets to Simply Graphing 
    #################################################################

    #_____________________________________________________________
    #Proceed to copy columns from demand_data_copy to production_data_copy
    #_________________________________________________________

    #columns_to_copy = ['EXPORT_BC', 'EXPORT_MT', 'EXPORT_SK', 'IMPORT_BC', 'IMPORT_MT', 'IMPORT_SK', 'Net_Export']
    columns_to_copy = [gbl_export_bc_label, gbl_export_mt_label, gbl_export_sk_label, gbl_import_bc_label, gbl_import_mt_label, gbl_import_sk_label, 'Net_Export']

    # Select the columns to copy from 'updated_demand_data'
    columns_to_add = gbl_processed_demand_data[columns_to_copy]

    # #Rename Net Exports to 'TIE_LINE'
    # processed_demand_data.rename(columns={})
    # df.rename(columns={"Net_Export": "TIE_LINE"})

    # #New
    # # Reindex 'columns_to_add' to match 'processed_production_data' indices
    # columns_to_add = columns_to_add.reindex(processed_production_data.index)

    # Reindex 'columns_to_add' to match 'processed_production_data' indices
    columns_to_add = columns_to_add.reindex(gbl_processed_production_data.index)

    # Rename 'Net_Export' to 'TIE_LINE'
    columns_to_add = columns_to_add.rename(columns={gbl_net_export_label: gbl_tie_line_label})

    #print(f" columns_to_add: {columns_to_add}")

    if gbl_processed_production_data.index.duplicated().any():
        print("Post Cleaning: Duplicates found in processed_production_data")
    else:
        print("Post Cleaning: No duplicates found in processed_production_data")
        
    if columns_to_add.index.duplicated().any():
        print("Post Cleaning: Duplicates found in columns_to_add")
    else:
        print("Post Cleaning: No duplicates found in columns_to_add")
    print("*" *90)

    # Concatenate the columns to 'updated_production_data' along axis=1 (columns)
    gbl_processed_production_data_with_import_exports = pd.concat([gbl_processed_production_data.copy(), columns_to_add.copy()], axis=1) #****************************

    gbl_processed_production_data_asset_ids_with_import_exports = gbl_processed_production_data_with_import_exports.columns
    #print(f" gbl_processed_production_data_asset_ids_with_import_exports: {gbl_processed_production_data_asset_ids_with_import_exports}")

    if gbl_processed_production_data_with_import_exports.index.duplicated().any():
        print("Post Cleaning/Post Column Add: Duplicates found in processed_production_data_with_import_exports")
    else:
        print("Post Cleaning/Post Column Add: No duplicates found in processed_production_data_with_import_exports")
        
        
    duplicate_indices = gbl_processed_production_data_with_import_exports.index.duplicated(keep=False)
    # Print duplicate rows
    #print(f" One More Check for Duplicates - processed_production_data_with_import_exports[duplicate_indices]: {processed_production_data_with_import_exports[duplicate_indices]}")

    ######################################    

    print(f" processed_demand_data.shape: {gbl_processed_demand_data.shape}")
    print(f" processed_demand_data: {gbl_processed_demand_data}")
    print("*" *90)
    print(f" processed_production_data_with_import_exports.shape: {gbl_processed_production_data_with_import_exports.shape}")
    print(f" processed_production_data_with_import_exports: {gbl_processed_production_data_with_import_exports}")
    print("*" *90)
    print(f" processed_price_data: {gbl_processed_price_data.shape}")
    print(f" processed_price_data: {gbl_processed_price_data}")
    print("*" *90)

    code_end()

    # return processed_price_data, processed_nat_gas_price, processed_production_data, processed_demand_data, processed_production_data_with_import_exports

#####################################################
# Final Prep for Production Data
#####################################################
def run_production_chart_final_prep():

    code_begin()
    global gbl_tech_type_column_hdr
    global gbl_processed_production_data_asset_ids_with_import_exports
    global gbl_processed_production_data_with_import_exports
    global gbl_wind_tech_type_label
    global gbl_solar_tech_type_label
    global gbl_non_wind_solar_tech_type_list

    #------------------------------------------------------
    # Step 1): Calculate and Store Hourly Production by Asset and Tech Type in Dictionaries
     #------------------------------------------------------

    #REVISED
    #------------------------------------------------------
    # Step 1a) Start with Hourly
    #------------------------------------------------------

    #gbl_hourly_production_by_asset_by_year = {}
    # print(f" processed_production_data_with_import_exports: {processed_production_data_with_import_exports}")
    # print(f" processed_production_data_with_import_exports: {processed_production_data_with_import_exports.shape}")
    # print(f" processed_production_data_with_import_exports: {processed_production_data_with_import_exports.info}")
    # print(f" gbl_processed_production_data_asset_ids_with_import_exports: {gbl_processed_production_data_asset_ids_with_import_exports}")

    # Find duplicate indices
    duplicate_indices = gbl_processed_production_data_with_import_exports.index.duplicated(keep=False)

    # Print duplicate rows
    #print(f" processed_production_data_with_import_exports[duplicate_indices]: {processed_production_data_with_import_exports[duplicate_indices]}")

    gbl_hourly_production_by_asset_by_year = {}

    new_columns = {}  # Dictionary to hold new columns to be added

    #------------------------------------------------------
    #Note
    # The up_to_date_production_data_asset_ids do not include the export data or the TIE_LINE category
    # The gbl_processed_production_data_asset_ids_with_import_exports does include this and this what we are
    # using to loop through the processed_production_data_with_import_exports data frame
    #------------------------------------------------------
    #for year in tqdm(range(2010, 2025)):
    for year in tqdm(range(gbl_first_year_data, gbl_last_year_data+1)):
        gbl_yearly_data = gbl_processed_production_data_with_import_exports.loc[gbl_processed_production_data_with_import_exports.index.year == year]

        #Code for spitting repowered asset time series data between prior and revised states
    #     for original_id, id_info in special_ids_dict.items():
    #         if original_id in yearly_df.columns:
    #             start_date = id_info['START_DATE']
    #             revised_id = id_info['revised_id']

    #             # Copy data from the start date onward from the original asset column
    #             copied_data = yearly_df[original_id][start_date:]
                
    #             new_columns[revised_id] = np.nan
                
    #             # Set the copied data in the original asset column to NaN from the start date
    #             #yearly_df.loc[start_date:, original_id] = np.nan

        
    #     # Concatenate new columns all at once
    #     yearly_df = pd.concat([yearly_df, pd.DataFrame(new_columns, index=yearly_df.index)], axis=1)
        
        #yearly_df = processed_production_data_with_import_exports[up_to_date_production_data_asset_ids].copy()
        #yearly_df = processed_production_data_with_import_exports[gbl_processed_production_data_asset_ids_with_import_exports].copy() #****************************
        
        
        # Store the modified hourly production data for this year
        gbl_hourly_production_by_asset_by_year[year] = gbl_yearly_data

        
    #print("gbl_hourly_production_by_asset_by_year Summary Table")
    #print_hourly_production_dict_by_asset_summary(gbl_hourly_production_by_asset_by_year)    

                
    #------------------------------------------------------
    # Step 1b) Now aggregate this data by tech type
    #------------------------------------------------------
 

    #Already defined above
    #all_asset_id = set(existing_production_df.columns).union(set(update_to_production_df.columns)) - {gbl_datetime_col_name}

    gbl_asset_to_tech_type = dict(zip(gv.gbl_meta_data_df[gbl_metadata_asset_id_column_hdr], gv.meta_data_df[gbl_metadata_tech_type_column_hdr]))
    #print(f" asset_to_tech_type: {asset_to_tech_type}")

    gbl_valid_asset_ids = gbl_processed_production_data_asset_ids_with_import_exports.copy() #****************************
    # Filter asset_to_tech_type to only include keys that are in valid_asset_ids
    gbl_filtered_asset_to_tech_type = {asset_id: tech_type for asset_id, tech_type in gbl_asset_to_tech_type.items() if asset_id in gbl_valid_asset_ids}


    tech_type_to_assets = {}

    for asset_id, tech_type in tqdm(gbl_filtered_asset_to_tech_type.items()):
        if tech_type not in tech_type_to_assets:
            tech_type_to_assets[tech_type] = []
        tech_type_to_assets[tech_type].append(asset_id)

    gbl_hourly_production_by_tech_by_year = {}

    for year, hourly_production_for_year in tqdm(gbl_hourly_production_by_asset_by_year.items()):
        gbl_hourly_production_by_tech = pd.DataFrame(index=hourly_production_for_year.index)

        for tech_type, asset_ids in tech_type_to_assets.items():
            # Use all asset IDs in the tech type mapping, as the DataFrame includes all assets
            aggregated_data = hourly_production_for_year[asset_ids].sum(axis=1)
            gbl_hourly_production_by_tech[tech_type] = aggregated_data

        # Store the hourly production data by tech type for this year
        gbl_hourly_production_by_asset_by_year[year] = gbl_hourly_production_by_tech   

    #------------------------------------------------------
    # Step 2): Calculate Monthly Production by Asset and Tech Type
    #------------------------------------------------------   
    gbl_monthly_production_by_asset = {}
    gbl_monthly_production_by_tech = {}


    for year in tqdm(gbl_hourly_production_by_asset_by_year):
        #.....................................................
        # Step 2 a) By Asset
        #..................................................... 
        gbl_monthly_production_by_asset[year] = gbl_hourly_production_by_asset_by_year[year].resample('M').sum()
        
        #.....................................................
        # Step 2 b) By Tech
        #.....................................................
        gbl_monthly_production_by_tech[year] = gbl_hourly_production_by_asset_by_year[year].resample('M').sum()

    # print(f" monthly_production_by_asset: {monthly_production_by_asset.head()}")
    # print(f" monthly_production_by_tech: {monthly_production_by_tech.head()}")

    #------------------------------------------------------     
    # Step 3): Calculate Quarterly Production By Asset
    #------------------------------------------------------
    # Resample to quarterly data
    gbl_quarterly_production_by_asset = {}
    gbl_quarterly_production_by_tech = {}

    #..................................................... 
    # Step 3 a) By Asset
    #.....................................................
    for year in tqdm(gbl_hourly_production_by_asset_by_year):
        # Quarterly aggregation
        gbl_quarterly_production_by_asset[year] = gbl_hourly_production_by_asset_by_year[year].resample('Q').sum()
    #.....................................................
    # Step 3 b) By Tech
    #.....................................................
    for year in tqdm(gbl_hourly_production_by_asset_by_year):
        # Quarterly aggregation
        gbl_quarterly_production_by_tech[year] = gbl_hourly_production_by_asset_by_year[year].resample('Q').sum()

    # Example to display the data for a particular year
    #print("Quarterly Production by Asset for a Year:", quarterly_production_by_asset.head())
    #print("Quarterly Production by Tech for a Year:", quarterly_production_by_tech.head())

    #------------------------------------------------------      
    # Step 4): Calculate Annual Production By Asset and Tech Type
    #------------------------------------------------------
    gbl_annual_production_by_asset = {}
    gbl_annual_production_by_tech = {}

    for year in tqdm(gbl_hourly_production_by_asset_by_year):
        # Annual aggregation
        #.....................................................
        # Step 4 a) By Asset
        #.....................................................
        gbl_annual_production_by_asset[year] = gbl_hourly_production_by_asset_by_year[year].resample('Y').sum()
        
        #.....................................................  
        # Step 4 b) By Tech
        #.....................................................
        gbl_annual_production_by_tech[year] = gbl_hourly_production_by_asset_by_year[year].resample('Y').sum()

    #print(f" annual_production_by_asset: {annual_production_by_asset}")
    #print(f" annual_production_by_tech: {annual_production_by_tech}")

    for year, df in tqdm(gbl_annual_production_by_asset.items()):
        if not df.index.is_unique:
            print(f"Non-unique indices found for the year {year}")
        else:
            print(f"No Non-unique indices were found for the year {year}")

    #print_annual_production_dict_by_asset_summary(annual_production_by_asset)
    #print_annual_production_dict_by_tech_summary(annual_production_by_tech)
    #print("*" *90)
    #------------------------------------------------------
    # Step 5): Calculate Annual Production By Tech Typeby Percentage Split of Tech Type
    #------------------------------------------------------
    # Aggregate to annual values and calculate percentage splits

    gbl_annual_production_by_tech_percentage = {}

    for year, df in tqdm(gbl_annual_production_by_tech.items()):
        # Divide each value by the sum of its row and multiply by 100 to get the percentage
        #.....................................................
        # Step 5 a) By Tech
        #.....................................................
        gbl_annual_production_by_tech_percentage[year] = df.divide(df.sum(axis=1), axis=0) * 100

    #------------------------------------------------------
    # Step 6): Calculate Annual Production By Tech Type Reduced and also by Percentage Split of Tech Type
    #------------------------------------------------------
    ## Initialize the reduced DataFrame with only 'WIND' and 'SOLAR' columns from the original
    gbl_annual_production_by_tech_reduced = {}
    gbl_annual_production_reduced_percentage = {}

    for year, df in tqdm(gbl_annual_production_by_tech.items()):
        # Check if 'WIND' and 'SOLAR' are in the DataFrame columns
        if gbl_wind_tech_type_label in df.columns and gbl_solar_tech_type_label in df.columns:
            # Select only 'WIND' and 'SOLAR' columns and copy
            reduced_df = df[[gbl_wind_tech_type_label, gbl_solar_tech_type_label]].copy()

            # Calculate the 'NON_WIND_SOLAR' production
            reduced_df[gbl_non_wind_solar_tech_type_list] = df.sum(axis=1) - reduced_df[gbl_wind_tech_type_label] - reduced_df[gbl_solar_tech_type_label]

            # Store the reduced DataFrame in the new dictionary
            gbl_annual_production_by_tech_reduced[year] = reduced_df
        else:
            # Handle the case where 'WIND' or 'SOLAR' is not present
            print(f"{gbl_wind_tech_type_label} or {gbl_solar_tech_type_label} not found in the columns for the year {year}")

    # Example to display the data for a particular year
    #print("Annual Production Reduced by Tech for a Year:", annual_production_by_tech_reduced[2020])


    for year, df in tqdm(gbl_annual_production_by_tech_reduced.items()):
        # Divide each value by the sum of its row and multiply by 100 to get the percentage
        #..................................................... 
        # Step 6 a) By Tech
        #.....................................................
        gbl_annual_production_reduced_percentage[year] = df.divide(df.sum(axis=1), axis=0) * 100

    # Display the resulting DataFrame
    #print(f" annual_production_by_tech_reduced: {annual_production_by_tech_reduced.head()}")
    #print(f" annual_production_tech_type_reduced_percentage: {annual_production_tech_type_reduced_percentage.head()}")

    #This is for printing only
    print_annual_production_dict_by_tech_summary(gbl_annual_production_by_tech_reduced)
    #print("*" *90)


    code_end()

    return

#####################################################
# Convert Production Data to DataFrames
#####################################################
def run_production_dict_convert_to_df():

    code_begin()
    
    global gbl_hourly_production_by_asset_by_year
    global gbl_hourly_production_by_tech_by_year
    global gbl_monthly_production_by_asset
    global gbl_monthly_production_by_tech
    global gbl_quarterly_production_by_asset
    global gbl_quarterly_production_by_tech
    global gbl_annual_production_by_asset
    global gbl_annual_production_by_tech
    global gbl_annual_production_by_tech_percentage
    
    
    
    # #By Asset
    # print("By Asset-Hourly")
    # for year, df in list(gbl_hourly_production_by_asset_by_year.items())[:3]:  # Check the first 3 years as an example
    #     print(year, df.index)
    # print("*" *90)
    # print("By Asset-Monthly")
    # for year, df in list(monthly_production_by_asset.items())[:3]:  # Check the first 3 years as an example
    #     print(year, df.index)
    # print("*" *90)
    # print("By Asset-Quarterly")
    # for year, df in list(quarterly_production_by_asset.items())[:3]:  # Check the first 3 years as an example
    #     print(year, df.index)
    # print("*" *90)
    # print("By Asset-Annually")
    # for year, df in list(annual_production_by_asset.items())[:3]:  # Check the first 3 years as an example
    #     print(year, df.index)
    # print("*" *90)
    # print("*" *90)
    # print("*" *90)
    # #By Tech Type
    # print("By Tech Type")
    # print("By Tech-Hourly")
    # for year, df in list(gbl_hourly_production_by_tech_by_year.items())[:3]:  # Check the first 3 years as an example
    #     print(year, df.index)
    # print("*" *90)
    # print("By Tech-Monthly")
    # for year, df in list(monthly_production_by_tech.items())[:3]:  # Check the first 3 years as an example
    #     print(year, df.index)
    # print("*" *90)
    # print("By Tech-Quarterly")
    # for year, df in list(quarterly_production_by_tech.items())[:3]:  # Check the first 3 years as an example
    #     print(year, df.index)
    # print("*" *90)
    # print("By Tech-Annually")
    # for year, df in list(annual_production_by_tech.items())[:3]:  # Check the first 3 years as an example
    #     print(year, df.index)

    #------------------------------------------------------


    # and ensure consistency across different time scales.

    pd.set_option('display.max_columns', None)


    #excluded_columns = ['Date_Begin_GMT', 'TIE_LINE', 'Year', 'Granularity']


    #column_headers = list(concatenated_gbl_hourly_production_by_asset_by_year_df.columns.values)

    #------------------------------------------------------
    #Hourly
    ##------------------------------------------------------

    #Asset - Hourly
    gbl_concatenated_hourly_production_by_asset_by_year_df = concatenate_with_year_column(gbl_hourly_production_by_asset_by_year, 'hourly')

    #Tech_Type - Hourly
    gbl_concatenated_hourly_production_by_tech_by_year_df = concatenate_with_year_column(gbl_hourly_production_by_tech_by_year, 'hourly')
    gbl_concatenated_hourly_production_by_tech_by_year_df = reorder_dataframe_columns(gbl_concatenated_hourly_production_by_tech_by_year_df, tech_type_desired_order)

    #------------------------------------------------------
    #Monthly
    #------------------------------------------------------
    #Asset - Monthly
    gbl_concatenated_monthly_production_by_asset_df = aggregate_to_frequency(gbl_hourly_production_by_asset_by_year, 'M')

    #Tech_Type - Monthly
    gbl_concatenated_monthly_production_by_tech_df = aggregate_to_frequency(gbl_hourly_production_by_tech_by_year, 'M')
    gbl_concatenated_monthly_production_by_tech_df = reorder_dataframe_columns(gbl_concatenated_monthly_production_by_tech_df, tech_type_desired_order)

    #------------------------------------------------------
    #Quarterly
    #------------------------------------------------------

    #Asset - Quarterly
    gbl_concatenated_quarterly_production_by_asset_df = aggregate_to_frequency(gbl_hourly_production_by_asset_by_year, 'Q')

    #Tech_Type - Quarterly
    gbl_concatenated_quarterly_production_by_tech_df = aggregate_to_frequency(gbl_hourly_production_by_tech_by_year, 'Q')
    gbl_concatenated_quarterly_production_by_tech_df = reorder_dataframe_columns(gbl_concatenated_quarterly_production_by_tech_df, tech_type_desired_order)

    #------------------------------------------------------
    #Annual
    #------------------------------------------------------
    #Asset - Annual
    gbl_concatenated_annual_production_by_asset_df = concatenate_annual_dataframes_with_year(gbl_annual_production_by_asset)

    #Tech_Type - Annual
    gbl_concatenated_annual_production_by_tech_df = concatenate_annual_dataframes_with_year(gbl_annual_production_by_tech)
    gbl_concatenated_annual_production_by_tech_df = reorder_dataframe_columns(gbl_concatenated_annual_production_by_tech_df, tech_type_desired_order)

    #Tech_Type % - Annual
    gbl_concatenated_annual_production_by_tech_percentage_df = concatenate_annual_dataframes_with_year(gbl_annual_production_by_tech_percentage)

    #Tech_Type (reduced) - Annual
    gbl_concatenated_annual_production_by_tech_reduced_df = concatenate_annual_dataframes_with_year(gbl_annual_production_by_tech_reduced)

    ###########################################################################
    # Save as CSV
    #Hourly by Asset
    #filename_csv = 'concatenated_gbl_hourly_production_by_asset_by_year_df.csv'
    #full_file_path_csv = create_file_path(base_output_directory_global , filename_csv)
    #concatenated_gbl_hourly_production_by_asset_by_year_df.to_csv(full_file_path_csv, index=True)
    #write_df_to_csv_with_progress(concatenated_gbl_hourly_production_by_asset_by_year_df, full_file_path_csv)

    save_dataframe_to_csv(gbl_concatenated_hourly_production_by_asset_by_year_df,'concatenated_gbl_hourly_production_by_asset_by_year_df.csv')

    #Monthly by Asset
    #filename_csv = 'concatenated_monthly_production_by_asset_df.csv'
    #full_file_path_csv = create_file_path(base_output_directory_global , filename_csv)
    #concatenated_monthly_production_by_asset_df.to_csv(full_file_path_csv, index=True)
    #write_df_to_csv_with_progress(concatenated_monthly_production_by_asset_df, full_file_path_csv)

    #Yearly by Asset
    # filename_csv = 'concatenated_annual_production_by_asset_df.csv'
    # full_file_path_csv = create_file_path(base_output_directory_global , filename_csv)
    # concatenated_annual_production_by_asset_df.to_csv(full_file_path_csv, index=True)
    # write_df_to_csv_with_progress(concatenated_annual_production_by_asset_df, full_file_path_csv)

    save_dataframe_to_csv(gbl_concatenated_annual_production_by_asset_df,'concatenated_annual_production_by_asset_df.csv')

    #Yearly by tech
    # filename_csv = 'concatenated_annual_production_by_tech_df.csv'
    # full_file_path_csv = create_file_path(base_output_directory_global , filename_csv)
    # concatenated_annual_production_by_tech_df.to_csv(full_file_path_csv, index=True)
    # write_df_to_csv_with_progress(concatenated_annual_production_by_tech_df, full_file_path_csv)

    save_dataframe_to_csv(gbl_concatenated_annual_production_by_tech_df,'concatenated_monthly_production_by_asset_df.csv')

    code_end()


    return