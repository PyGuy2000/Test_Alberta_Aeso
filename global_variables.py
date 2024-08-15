
import os
import pandas as pd
# from initializer import(
#     gbl_base_output_directory_global, 
#     gbl_base_input_directory_global, 
#     gbl_ide_option, 
#     gbl_csv_folder, 
#     gbl_image_folder)
import initializer as init # aliasing the initializer module as init
import json


#########################################
# Set up file dictionary 
#########################################
# data_frames = {
#     'gbl_pool_price_data': (gbl_pool_price_data, '%Y-%m-%d %H:%M'),
#     'gbl_up_to_date_production_data': (gbl_up_to_date_production_data, '%m/%d/%Y %H:%M'),
#     'gbl_demand_data': (gbl_demand_data, '%Y-%m-%d %H:%M'),
#     'gbl_hourly_nat_gas_price_data': (gbl_hourly_nat_gas_price_data, '%m/%d/%Y %H:%M'),
#     'glb_meta_data': (gbl_meta_data, '%m/%d/%Y %H:%M')
# }

#########################################
# Function to extract data_source dictionary details
########################################
# Load the JSON file and assign it to a global variable
with open('file_data.json', 'r') as f:
    data_sources = json.load(f)
    print(data_sources)

# def get_data_source_details(source_name):
#     source_details = data_sources.get(source_name, {})
#     file_type = source_details.get("file_type")
#     sub_folder = source_details.get("sub_folder")
#     template_file = source_details.get("template_file")
#     path = source_details.get("path")
#     date_format = source_details.get("date_format")
#     existing_date_col = source_details.get("existing_date_col")
#     existing_date_col_name = source_details.get("existing_date_col_name")
#     column_names = source_details.get("column_names")
#     return file_type, sub_folder, path, template_file, date_format, existing_date_col, existing_date_col_name, column_names

def get_data_source_details(source_name):
    source_details = data_sources.get("data_sources", {}).get(source_name, {})
    file_type = source_details.get("file_type")
    sub_folder = source_details.get("sub_folder")
    path = source_details.get("path")
    template_file = source_details.get("template_file")
    date_format = source_details.get("existing_date_format")  # Adjusted key name
    revised_date_col = source_details.get("revised_date_col")
    existing_mptdate_col = source_details.get("existing_mptdate_col")
    existing_mptdate_col_name = source_details.get("existing_mptdate_col_name")
    column_names = source_details.get("column_names")
    return file_type, sub_folder, path, template_file, date_format, existing_mptdate_col, revised_date_col, existing_mptdate_col_name, column_names

#########################################
# Declare known Global Variables 
#########################################

#Time Formatting
gbl_datetime_col_name = 'DateTime'
gbl_datetime_hourly_timeseries_format = '%m/%d/%Y %H:%M' #This is int64[ns] format

gbl_first_year_data = 2010
gbl_last_year_data = 2023
gbl_last_year_data_for_graphing = 2023
gbl_last_month_data = 1

#---------------------------------------
#  Existing Production Data and Update for Appending
#---------------------------------------
json_query = 'gbl_existing_production_data'
gbl_production_existing_file_type, gbl_sub_folder_existing_production,  gbl_path_existing_production, glb_existing_production_template_file, gbl_existing_production_existing_date_format, \
    gbl_dateMST_label_existing_production, revised_date_col_existing_production, gbl_production_existing_mptdate_col_name, gbl_existing_production_column_names = get_data_source_details(json_query)

json_query = 'gbl_update_to_production_data'
gbl_update_to_production_data_file_type, gbl_sub_folder_update_to_production, gbl_path_update_to_production, gbl_update_to_production_data_template_file, gbl_update_to_production_date_format, \
    gbl_dateMST_label_update_to_production, revised_date_col_update_to_production, gbl_update_to_production_data_col_name, gbl_update_to_production_column_names = get_data_source_details(json_query)
    
json_query = 'gbl_up_to_date_production_data'
gbl_up_to_date_production_file_type, gbl_sub_folder_up_to_date_production,  gbl_path_up_to_date_production, glb_up_to_date_production_template_file, gbl_up_to_date_production_existing_date_format, \
    gbl_dateMST_label_up_to_date_production, revised_date_col_up_to_date_production, gbl_up_to_date_production_existing_mptdate_col_name, gbl_up_to_date_production_existing_column_names = get_data_source_details(json_query)

# gbl_production_existing_date_format = '%m/%d/%Y %H:%M'
# gbl_dateUTC_label_existing_production  = 'begin_date_utc'
# gbl_dateMST_label_existing_production = 'begin_date_mpt'


column_names = []
#---------------------------------------
# Meta Data
#---------------------------------------
json_query = 'gbl_meta_data'

gbl_metadata_file_type, gbl_metadata_sub_folder,  gbl_metadata_path, glb_metadata_template_file, gbl_metadata_existing_date_format, \
    gbl_dateMST_label_metadata, revised_date_col_gbl_dateMST_label_metadata, gbl_metadata_date_col_name, gbl_production_existing_column_names = get_data_source_details(json_query)

#gbl_metadata_existing_date_format = '%m/%d/%Y'
gbl_data_types = {
    'START_YEAR': 'int64',
    'RETIREMENT_YEAR': 'int64',
}

#Technology Labels
gbl_metadata_coal_tech_type_label = 'COAL'
gbl_metadata_cogeneration_tech_type_label = 'COGENERATION'
gbl_metadata_combined_cycle_tech_type_label = 'COMBINED_CYCLE'
gbl_metadata_hydro_tech_type_label = 'HYDRO'
gbl_metadata_dual_fuel_tech_type_label = 'DUAL_FUEL'
gbl_metadata_simple_cycle_tech_type_label = 'SIMPLE_CYCLE'
gbl_metadata_gas_fired_steam_tech_type_label = 'GAS_FIRED_STEAM'
gbl_metadata_other_tech_type_label = 'OTHER'
gbl_metadata_solar_tech_type_label = 'SOLAR'
gbl_metadata_wind_tech_type_label = 'WIND'
gbl_metadata_unknown_tech_type_label = 'UNKNOWN'
gbl_metadata_energy_storage_tech_type_label = 'ENERGY_STORAGE'
gbl_metadata_tie_line_tech_type_label = 'TIE_LINE'
gbl_metadata_btf_generation_tech_type_label = 'BTF_GENERATION'   
gbl_metadata_non_wind_solar_tech_type_list = 'NON_WIND_SOLAR'

#Fuel Labels
gbl_metadata_coal_fuel_type_label = 'COAL'
gbl_metadata_gas_fuel_type_label = 'GAS'
gbl_metadata_dual_fuel_fuel_type_label = 'DUAL_FUEL'
gbl_metadata_hydro_fuel_type_label = 'HYDRO'
gbl_metadata_other_fuel_type_label = 'OTHER'
gbl_metadata_solar_fuel_type_label = 'SOLAR'
gbl_metadata_wind_fuel_type_label = 'WIND'
gbl_metadata_unknown_fuel_type_label = 'UNKNOWN'
gbl_metadata_energy_storage_fuel_type_label = 'ENERGY_STORAGE'
gbl_metadata_tie_line_fuel_type_label = 'TIE_LINE'

gbl_metadata_asset_id_column_hdr = 'ASSET_ID'
gbl_metadata_asset_name_long_column_hdr = 'ASSET_NAME_LONG'
gbl_metadata_asset_name_column_hdr = 'ASSET_NAME'
gbl_metadata_repower_flag_column_hdr = 'REPOWER_FLAG'
gbl_metadata_prelinminary_status_column_hdr = 'PRELINMINARY_STATUS'
gbl_metadata_status_check_column_hdr = 'STATUS_CHECK'
gbl_metadata_status_column_hdr = 'STATUS'
gbl_metadata_fuel_type_column_hdr = 'FUEL_TYPE'
gbl_metadata_tech_type_column_hdr = 'TECH_TYPE'
gbl_metadata_fuel_sub_type_column_hdr = 'FUEL_SUB_TYPE'
gbl_metadata_maximum_capability_column_hdr = 'MAXIMUM_CAPABILITY'
gbl_metadata_mc_column_hdr = 'MC'
gbl_metadata_dc_column_hdr = 'DC'
gbl_metadata_net_mc_column_hdr = 'NET_MC'
gbl_metadata_net_to_grid_asset_column_hdr = 'NET_TO_GRID_ASSET'
gbl_metadata_ft_column_hdr = 'FT'
gbl_metadata_location_column_hdr = 'LOCATION'
gbl_metadata_latitude_column_hdr = 'LATITUDE'
gbl_metadata_longitude_column_hdr = 'LONGITUDE'
gbl_metadata_gps_status_column_hdr = 'GPS_STATUS'
gbl_metadata_start_date_column_hdr = 'START_DATE'
gbl_metadata_retirement_date_column_hdr = 'RETIREMENT_DATE'
gbl_metadata_start_year_column_hdr = 'START_YEAR'
gbl_metadata_retirement_year_column_hdr = 'RETIREMENT_YEAR'
gbl_metadata_min_up_time_column_hdr = 'MIN_UP_TIME'
gbl_metadata_max_down_time_column_hdr = 'MAX_DOWN_TIME'
gbl_metadata_ramp_up_rate_column_hdr = 'RAMP_UP_RATE'
gbl_metadata_ramp_down_rate_column_hdr = 'RAMP_DOWN_RATE'
gbl_metadata_location_mpid_column_hdr = 'LOCATION_MPID'
gbl_metadata_pss_ebus_column_hdr = 'PSS_EBUS'
gbl_metadata_aeso_technology_column_hdr = 'AESO_TECHNOLOGY'
gbl_metadata_transmission_area_name_column_hdr = 'TRANSMISSION_AREA_NAME'
gbl_metadata_transmission_area_number_column_hdr = 'TRANSMISSION_AREA_NUMBER'
gbl_metadata_asset_owner_column_hdr = 'ASSET_OWNER'
gbl_metadata_pool_participant_id_column_hdr = 'POOL_PARTICIPANT_ID'
gbl_metadata_sts_column_hdr = 'STS'
gbl_metadata_fixed_om_cost_column_hdr = 'FIXED_OM_COST'  
gbl_metadata_var_om_cost_column_hdr = 'VAR_OM_COST'  
gbl_metadata_heat_rate_column_hdr = 'HEAT_RATE'  
gbl_metadata_fuel_price_type_column_hdr = 'FUEL_PRICE_TYPE'  
gbl_metadata_fuel_price_column_hdr = 'FUEL_PRICE'
gbl_metadata_starts_column_hdr = 'STARTS'
gbl_metadata_stops_column_hdr = 'STOPS'
gbl_metadata_start_costs_column_hdr = 'START_COSTS'
gbl_metadata_emission_intensity_column_hdr = 'EMISSION_INTENSITY' 
gbl_metadata_taxable_emissions_column_hdr = 'TAXABLE_EMISSIONS'  
gbl_metadata_marginal_cost_real_column_hdr = 'MARGINAL_COST _REAL'  
gbl_metadata_index_type_column_hdr = 'INDEX_TYPE'
gbl_metadata_marginal_cost_column_hdr = 'MARGINAL_COS'  
gbl_metadata_total_costs_column_hdr = 'TOTAL_COSTS'

# Status
gbl_metadata_development_status_label = 'DEVELOPMENT'  
gbl_metadata_operating_repowered_status_label = 'OPERATING/REPOWERED'
gbl_metadata_retired_status_label = 'RETIRED'

column_names = ['ASSET_ID', 'ASSET_NAME_LONG', 'ASSET_NAME', 'REPOWER_FLAG', 'PRELINMINARY_STATUS', 'STATUS_CHECK', 'STATUS', 'FUEL_TYPE', \
    'TECH_TYPE', 'FUEL_SUB_TYPE', 'MAXIMUM_CAPABILITY', 'MC', 'DC', 'NET_MC', 'NET_TO_GRID_ASSET', 'FT', 'LOCATION', 'LATITUDE', 'LONGITUDE', \
        'GPS_STATUS', 'START_DATE', 'RETIREMENT_DATE', 'START_YEAR', 'RETIREMENT_YEAR', 'MIN_UP_TIME', 'MAX_DOWN_TIME', 'RAMP_UP_RATE', 'RAMP_DOWN_RATE', \
            'LOCATION_MPID', 'PSS_EBUS', 'AESO_TECHNOLOGY', 'TRANSMISSION_AREA_NAME', 'TRANSMISSION_AREA_NUMBER', 'ASSET_OWNER', 'POOL_PARTICIPANT_ID', 'STS', \
                'FIXED_OM_COST', 'VAR_OM_COST', 'HEAT_RATE', 'FUEL_PRICE_TYPE', 'FUEL_PRICE', 'STARTS', 'STOPS', 'START_COSTS', 'EMISSION_INTENSITY', 'TAXABLE_EMISSIONS', \
                    'MARGINAL_COST _REAL', 'INDEX_TYPE', 'MARGINAL_COS', 'TOTAL_COSTS']

#---------------------------------------
# Exports/Imports
#---------------------------------------
gbl_net_export_label = "Net_Export" 
gbl_tie_line_label = "TIE_LINE"

gbl_export_bc_label = 'EXPORT_BC' 
gbl_export_mt_label = 'EXPORT_MT' 
gbl_export_sk_label = 'EXPORT_SK' 
gbl_import_bc_label = 'IMPORT_BC' 
gbl_import_mt_label = 'IMPORT_MT' 
gbl_import_sk_label = 'IMPORT_SK'
gbl_export_imports_category_list = [
    gbl_export_bc_label,
    gbl_export_mt_label, 
    gbl_export_sk_label, 
    gbl_import_bc_label, 
    gbl_import_mt_label, 
    gbl_import_sk_label
]

#---------------------------------------
# Pool Price
#---------------------------------------
json_query = 'gbl_pool_price_data'
gbl_pool_price_file_type, glb_pool_price_sub_folder, gbl_pool_price_path, gbl_pool_price_template_file, gbl_pool_price_existing_date_format, \
    gbl_dateMPT_label_pool_price, revised_date_col_gbl_dateMST_label_pool_price, gbl_pool_price_existing_mptdate_col_name, gbl_pool_price_existing_column_names = get_data_source_details(json_query)

# gbl_pool_price_existing_date_format = '%Y-%m-%d %H:%M'
# gbl_subfolder_name_pool_price = "aeso-spot-prices-2000-2023"
# gbl_pool_price_template  = "pool_price_data_"
# gbl_pool_price_template  = "pool_price_data_"
# gbl_dateUTC_label_pool_price  = 'begin_date_utc'
# gbl_dateMPT_label_pool_price = 'begin_date_mpt'
# gbl_subfolder_name_pool_price = "aeso-spot-prices-2000-2023"
# column_names = ["pool_price", "forecast_pool_price", "rolling_30day_avg"]


#--------------------------------------
# Demand Data
#--------------------------------------
json_query = 'gbl_demand_data'
gbl_demand_file_type, gbl_demand_sub_folder, gbl_demand_path, gbl_demand_template_file, gbl_demand_existing_date_format, \
    gbl_dateMPT_label_ail_demand, revised_date_col_gbl_dateMST_label_ail_demand, gbl_demand_existing_mptdate_col_name, gbl_demand_existing_column_names = get_data_source_details(json_query)
    
# gbl_demand_existing_date_format = '%Y-%m-%d %H:%M'
# gbl_demand_template ="Metered_Demand_"
# gbl_actual_ail_demand_label = 'ACTUAL_AIL'
# gbl_dateUTC_label_ail_demand = 'begin_datetime_utc'
# gbl_dateMPT_label_ail_demand = 'begin_datetime_mpt'
# gbl_subfolder_name_demand = "aeso-metered-demand-2000-to-2023"
# column_names = ['begin_datetime_utc', 'begin_datetime_mpt', 'alberta_internal_load', 'forecast_alberta_internal_load']

# Natural Gas Prices (Daily)
#---------------------------------------
json_query = 'gbl_hourly_nat_gas_price_data'
gbl_natgas_file_type, gbl_natgas_sub_folder, gbl_natgas_path, gbl_natgas_template_file, gbl_natgas_existing_date_format, \
    gbl_dateMPT_label_natural_gas, revised_date_col_gbl_dateMST_label_natural_gas, gbl_natgas_existing_mptdate_col_name, gbl_natgas_existing_column_names = get_data_source_details(json_query)
    
# gbl_natgas_existing_date_format = ""
# gbl_date_label_natural_gas = 'DATE_BEGIN_LOCAL'
#column_names = ["2000", "2001", "2002", "2003", "2004", "2005", "2006", "2007", "2008", "2009", "2010", "2011", "2012", "2013", "2014", "2015", "2016", "2017", "2018", "2019", "2020", "2021", "2022", "2023", "2024"]
#---------------------------------------
# Merit Order
#---------------------------------------
json_query = 'gbl_merit_order_data'

gbl_merit_order_file_type, gbl_merit_order_sub_folder, gbl_merit_order_path, gbl_merit_order_template_file, gbl_merit_order_existing_date_format, \
    gbl_dateMPT_label_merit_order, revised_date_col_gbl_dateMST_label_merit_order, gbl_merit_order_existing_mptdate_col_name, gbl_merit_order_existing_column_names = get_data_source_details(json_query)

# gbl_merit_order_existing_date_format = "%d%b%y:%H:%M:%S"
# gbl_settlement_interval_start_gmt_column_hdr = 'Settlement Interval Start (GMT)'
# gbl_settlement_interval_start_mst_column_hdr = 'Settlement Interval Start (MST)'
# gbl_serialasset_short_name_column_hdr = 'Serial,Asset Short Name'
# gbl_mpid_name_column_hdr = 'MPID Name'
# gbl_importexport_column_hdr = 'Import/Export'
# gbl_block_number_column_hdr = 'Block Number'
# gbl_flexible_column_hdr = 'Flexible'
# gbl_offer_price_mwh_column_hdr = 'Offer Price ($/MWh)'
# gbl_block_size_mw_column_hdr = 'Block Size (MW)'
# gbl_available_power_mw_column_hdr = 'Available Power (MW)'
# gbl_dispatched_power_mw_column_hdr = 'Dispatched Power (MW)'
# gbl_capability_mw_column_hdr = 'Capability (MW)'
# gbl_cumulative_dispatched_mw_per_mpid_column_hdr = 'Cumulative Dispatched MW per MPID'
# gbl_supply_shortfall_management_step_column_hdr = 'Supply Shortfall Management Step'
# gbl_activation_price_column_hdr = 'Activation Price'
# column_names = ['Settlement Interval Start (GMT)', 'Settlement Interval Start (MST)', 'Serial,Asset Short Name', 'MPID Name', 'Import/Export', 'Block Number', 'Flexible', 'Offer Price ($/MWh)', \
#     'Block Size (MW)', 'Available Power (MW)', 'Dispatched Power (MW)', 'Capability (MW)', 'Cumulative Dispatched MW per MPID', 'Supply Shortfall Management Step', 'Activation Price']
#---------------------------------------
# Carbon Data
#---------------------------------------
gbl_carbon_tax_annual_dict = {
    '2001': 0,
    '2002': 0,
    '2003': 0,
    '2004': 0,
    '2005': 0,
    '2006': 0,
    '2007': 15,
    '2008': 15,
    '2009': 15,
    '2010': 15,
    '2011': 15,
    '2012': 15,
    '2013': 15,
    '2014': 15,
    '2015': 15,
    '2016': 20,
    '2017': 30,
    '2018': 30,
    '2019': 30,
    '2020': 30,
    '2021': 40,
    '2022': 50,
    '2023': 65,
    '2024': 80,
    '2025': 95,
    '2026': 110
}
#---------------------------------------
# GeoSpatial Datea
#---------------------------------------
#AESO Planning Area Coordinates
gbl_planning_area_column_hdr = 'PLANNING_AREA'
gbl_planning_area_number_column_hdr = 'PLANNING_AREA_NUMBER'
gbl_planning_area_name_column_hdr = 'PLANNING_AREA_NAME'
gbl_planning_area_shape_column_hdr = 'geometry'

#Transmission Area Coordinates
gbl_transmission_area_column_hdr = 'TRANSMISSION_AREA'
gbl_transmission_area_number_column_hdr = 'TRANSMISSION_AREA_NUMBER'
gbl_transmission_area_name_column_hdr = 'TRANSMISSION_AREA_NAME'
gbl_transmission_area_shape_column_hdr = 'geometry'

#Transmission Line Coordinates
gbl_transmission_line_column_hdr = 'TRANSMISSION_LINE'
gbl_transmission_line_number_column_hdr = 'TRANSMISSION_LINE_NUMBER'
gbl_transmission_line_name_column_hdr = 'TRANSMISSION_LINE_NAME'
gbl_transmission_line_shape_column_hdr = 'geometry'

#Substation Coordinates
gbl_substation_column_hdr = 'SUBSTATION'
gbl_substation_number_column_hdr = 'SUBSTATION_NUMBER'
gbl_substation_name_column_hdr = 'SUBSTATION_NAME'
gbl_substation_shape_column_hdr = 'geometry'

#STS Loss Factor Data
gbl_sts_loss_factor_column_hdr = 'STS'
gbl_sts_loss_factor_shape_column_hdr = 'geometry'

#---------------------------------------
# AESO CSC Report Page
#---------------------------------------
#

#---------------------------------------
# LCOE Analysis
#---------------------------------------

#########################################
# Initialize Global Variables Calculated within the setup_global_variables function()
#########################################

gbl_existing_production_df = None
gbl_update_to_production_df = None
gbl_meta_data_df = None
gbl_daily_nat_gas_prices_df = None
gbl_substation_shape_file_path = None
gbl_transmission_shape_file_path = None
gbl_substation_capability_file_path = None
gbl_transmission_capability_file_path = None
gbl_sts_capability_file_path = None
gbl_planning_area_file_path = None
gbl_mock_gen_gps_data = None
gbl_ercot_demand_data_2023 = None
gbl_aseso_csd_report_servlet = None


#########################################
# Functions()
#########################################
#def create_path_2(input_dir, filename, subfolder_name=''):
def create_path_2(input_dir,filename, subfolder_name=''):
    full_path = os.path.normpath(os.path.join(input_dir, subfolder_name, filename))
    return full_path

#def read_from_csv_input_folder_2(ide_option, gbl_base_input_directory_global, filename, subfolder_name=''):
def read_from_csv_input_folder_2(filename, subfolder_name=''):
    if init.gbl_ide_option == 'vscode':
        full_path = create_path_2(init.gbl_base_input_directory_global, filename, subfolder_name)
    elif init.gbl_ide_option == 'jupyter_notebook':
        # Additional code for Jupyter environment
        pass
    elif init.gbl_ide_option == 'kaggle':
        full_path = create_path_2(init.gbl_base_input_directory_global, filename, subfolder_name)

    print(f" full_path: {full_path}")

    if not os.path.exists(full_path):
        print("Error: The file does not exist at the specified path.")
        return None

    df = pd.read_csv(full_path, low_memory=False)
    print(f"{filename} loaded from input folder...")
    return df



#def setup_global_variables(ide_option, base_input_directory_global, input_dir):
def setup_global_variables():
    # Declare global variables
    #global gbl_ide_option
    global gbl_existing_production_df
    global gbl_update_to_production_df
    global gbl_meta_data_df
    global gbl_daily_nat_gas_prices_df
    global gbl_substation_shape_file_path
    global gbl_transmission_shape_file_path
    global gbl_substation_capability_file_path
    global gbl_transmission_capability_file_path
    global gbl_sts_capability_file_path
    global gbl_planning_area_file_path
    global gbl_mock_gen_gps_data
    global gbl_ercot_demand_data_2023
    global gbl_aeso_csd_report_servlet

    #gbl_ide_option = ide_option

    # Load CSV files
    #______________________________________________________________________________
    #Existing Production Data and Update for Appending
    #______________________________________________________________________________
    #File Path for Existing Production Data
    #gbl_existing_production_df = read_from_csv_input_folder_2(ide_option, base_input_directory_global, 'Hourly_Metered_Volumes_and_Pool_Price_and_AIL 20100101 to 20231231.csv', 'metered-volume-source-files')
    gbl_existing_production_df = read_from_csv_input_folder_2('Hourly_Metered_Volumes_and_Pool_Price_and_AIL 20100101 to 20231231.csv', 'metered-volume-source-files')
    # Ensure they are not None
    assert gbl_existing_production_df is not None, "gbl_existing_production_df is not initialized properly"
    print(f" existing_production_df.colunms: {gbl_existing_production_df.columns}")

    #File Path for Update to Production Data
    #gbl_update_to_production_df = read_from_csv_input_folder_2(ide_option, base_input_directory_global,'Consolidated Generation Metered Volumes 20240101 to 20240702.csv', 'metered-volume-source-files')
    gbl_update_to_production_df = read_from_csv_input_folder_2('Consolidated Generation Metered Volumes 20240101 to 20240702.csv', 'metered-volume-source-files')
    # Ensure they are not None
    assert gbl_update_to_production_df is not None, "gbl_update_to_production_df is not initialized properly"
    print(f" update_to_production_df.columns: {gbl_update_to_production_df.columns}")

    #______________________________________________________________________________
    # Load Generator Meta Data Files
    #______________________________________________________________________________

    #File Path for Generator Metadata
    #gbl_meta_data_df = read_from_csv_input_folder_2(ide_option, base_input_directory_global,  'generatorMetadata_20240617.csv','source-meta-data-files')
    gbl_meta_data_df = read_from_csv_input_folder_2('generatorMetadata_20240617.csv','source-meta-data-files')
    print(gbl_meta_data_df)
    # Convert date columns separately with the known format
    gbl_meta_data_df[gbl_metadata_start_date_column_hdr] = pd.to_datetime(gbl_meta_data_df[gbl_metadata_start_date_column_hdr], format=gbl_metadata_existing_date_format)
    gbl_meta_data_df[gbl_metadata_retirement_date_column_hdr] = pd.to_datetime(gbl_meta_data_df[gbl_metadata_retirement_date_column_hdr], format=gbl_metadata_existing_date_format)

    #______________________________________________________________________________
    #Pool Price
    #______________________________________________________________________________
    #File Path for Pool Price
    #handled later in code using a pool_price_template object

    #_________________________________________________________________________________
    #Natural Gas Prices (Daily)
    #______________________________________________________________________________
    #File Path for Daily Natural Gas Prices
    #gbl_daily_nat_gas_prices_df = read_from_csv_input_folder_2(ide_option, base_input_directory_global,'AECO Natural Gas 2000 to 2024 Daily 062524.csv','aeco-daily-natural-gas-prices-2000-to-2024')
    gbl_daily_nat_gas_prices_df = read_from_csv_input_folder_2('AECO Natural Gas 2000 to 2024 Daily 062524.csv','aeco-daily-natural-gas-prices-2000-to-2024')
    #______________________________________________________________________________
    #Demand Data
    #______________________________________________________________________________
    #File Path for Demand Data
    #handled later in code
    #______________________________________________________________________________
    #Substation and Transmission Shape Files
    #______________________________________________________________________________
    #File Path for Substation and Transmission Shape Files
    gbl_substation_shape_file_path = create_path_2(init.gbl_input_dir, 'Substations.shp', 'aeso-substation-and-transmission-shape-files' )
    gbl_transmission_shape_file_path = create_path_2(init.gbl_input_dir, 'Transmission Lines.shp','aeso-substation-and-transmission-shape-files')
    #Date Labels for Substation and Transmission Shape Files
    #None
    #______________________________________________________________________________
    #Substation and Transmission Shape Data Files
    #______________________________________________________________________________
    #File Path for Substation and Transmission Shape Data Files
    gbl_substation_capability_file_path = create_path_2(init.gbl_input_dir, 'Substation Capability Data.csv','alberta-transmission-and-substation-data')
    gbl_transmission_capability_file_path = create_path_2(init.gbl_input_dir,  'Transmission Capability Data.csv','alberta-transmission-and-substation-data')
    gbl_sts_capability_file_path = create_path_2(init.gbl_input_dir,  'STS Loss Factor Data.csv','alberta-transmission-and-substation-data')
    #Date Labels for Substation and Transmission Shape Data Files
    #None

    #______________________________________________________________________________
    #AESO Planning Area Coordinates
    #______________________________________________________________________________
    #File Path for AESO Planning Area Coordinates
    gbl_planning_area_file_path = create_path_2(init.gbl_input_dir,'AESO_Planning_Areas.shp', 'aeso-planning-areas')
    #Date Labels for AESO Planning Area Coordinates
    #None
    #______________________________________________________________________________
    #Mock GPS Data
    #______________________________________________________________________________
    #File Path for Mock GPS Data
    gbl_mock_gen_gps_data = create_path_2(init.gbl_input_dir,'Mock GPS Coordinates 20240404.csv','source-meta-data-files')
    #Date Labels for Mock GPS Data
    #None
    #______________________________________________________________________________
    #ERCOT Demand Data
    #______________________________________________________________________________
    #File Path for ERCOT Demand Data
    gbl_ercot_demand_data_2023 = create_path_2(init.gbl_input_dir, 'Native_Load_2023.xlsx', 'ercot-demand-data')
    #Date Labels for ERCOT Demand Data
    #None
    #_____________________________________________________________________________
    #AESO CSC Report Page 
    #______________________________________________________________________________
    #File Path for AESO CSC Report Page
    gbl_aeso_csd_report_servlet = create_path_2(init.gbl_input_dir, 'CSDReportServlet_20240718.htm', 'aeso-website-structure')
    #Date Labels for AESO CSC Report Page
    #None
    
        
    #code_end()
    return