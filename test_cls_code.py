from class_objects.cls_power_data import PowerMarketData
from class_objects.graph_config import GraphConfig
from class_objects.api_client import APIClient
from api_tools import get_api_credentials, build_api_request_repository
import os
import sys
import pandas as pd
import datetime
from dotenv import load_dotenv
import Utilities_API
from Utilities_API import (
    print_directory_tree,
    print_folder_list,
    remove_folder_contents,
    create_path,
    fetch_data,
    create_sqlite_table,
    save_to_sqlite,
    execute_sql_query,
)

#########################################
def main():
    # data_sources = {
    # 'gbl_existing_production_df': 'Hourly_Metered_Volumes_and_Pool_Price_and_AIL 20100101 to 20231231.csv',
    # 'gbl_update_to_production_df': 'Consolidated Generation Metered Volumes 20240101 to 20240702.csv',
    # 'gbl_meta_data_df': 'eneratorMetadata_20240617.csv',
    # 'gbl_daily_nat_gas_prices_df': 'AECO Natural Gas 2000 to 2024 Daily 062524.csv',
    # 'gbl_substation_shape_file_path': 'path_to_hourly_generation_data.csv',
    # 'gbl_transmission_shape_file_path' : 'STS Loss Factor Data.csv',
    # 'gbl_substation_capability_file_path' : 'Substation Capability Data.csv',
    # 'gbl_transmission_capability_file_path' : 'Transmission Capability Data.csv',
    # 'gbl_sts_capability_file_path' : 'STS Loss Factor Data.csv',
    # 'gbl_planning_area_file_path' : 'AESO_Planning_Areas.shp',
    # 'gbl_mock_gen_gps_data' : '........',
    # 'gbl_ercot_demand_data_2023' : 'input_data\ercot-demand-data\Native_Load_2023.xlsx',
    # 'gbl_aseo_csd_report_servlet0' : 'CSDReportServlet.htm',
    # ' ' : '........',
    # ' ' : '........',
    # ' ' : '........',
    # ' ' : '........',
    # ' ' : '........',
    # ' ' : '........',
    # # Add other data sources as needed
    # }

    # annual_files = [
    #     'path_to_annual_file_2000.csv',
    #     'path_to_annual_file_2001.csv',
    #     # Add other annual file paths as needed
    # ]

    # meta_data_sources = {
    #     'generator_meta': 'generatorMetadata_20240617.csv',
    #     # Add other meta data sources as needed
    # }



    # Create instance of the class
    api_client = APIClient(base_url="https://api.example.com")
    power_data = PowerMarketData()
    graph_config = GraphConfig()
    
    # Create Instance of Power Data class
    power_data = PowerMarketData()
    # Call class methods
    power_data.load_data(data_sources)
    power_data.load_meta_data(meta_data_sources)
    power_data.serialize_merit_order_data('merit_order')
    power_data.aggregate_annual_files(annual_files, 'aggregated_annual_data')
    power_data.merge_data_frames()
    power_data.convert_column_headers()
    power_data.standardize_date_columns()
    power_data.clean_data()  # New method to prepare and clean data
    power_data.preprocess_data_frames()  # New preprocessing method
    power_data.process_data()
    power_data.summarize_data()
    power_data.create_visualizations()
    power_data.export_to_csv('output_path')
    power_data.export_to_sql('database_path.db')

    # # Filtering example
    # filtered_data = power_data.filter_data(start_date='2020-01-01', end_date='2021-01-01', asset_id='A1')
    # print(filtered_data)
    
    # # Create an animation example
    # power_data.create_animation(key='hourly_demand', column='MEAN', title='Hourly Demand Over Time', save_path='hourly_demand_animation.gif')
    
    # # Example API usage
    # api_data = power_data.fetch_data_from_api(endpoint='data_endpoint', params={'param1': 'value1'})
    # print(api_data)
    
    # power_data.export_data('output_path')
    # power_data.populate_sql('sql_connection_string')
    
    ##############################################################################
    #Active API Calls
    ###########################################################################
        
    api_activation_dict = {
        'pool_participant_data_state': False,
        'operating_reserve_offer_control_data_state': False,
        'actual_forecast_report_data_state': False,
        'asset_list_data_state': False,
        'generators_above_5MW_data_state': False,
        'historical_spot_price_specific_date_and_range_state': False,
        'historical_spot_price_specific_date_state': False,
        'merit_order_data_state': False,
        'metered_volume_data_state': True,
        'supply_demand_data_generation_state': False,
        'supply_demand_data_intertie_state': False,
        'supply_demand_data_summary_state': False,
        'system_marginal_price_data_state': False
    }

    # Load .env file
    load_dotenv()

    #------------------------------------------------
    # Get API credentials function
    def get_api_credentials(service):
        # Implement this function based on your requirement
        # Return API key, base URL, and output folder path for the service
        pass
    #------------------------------------------------
    # Build API request repository function
    def build_api_request_repository(api_activation_dict, aeso_key, base_url, start_date, end_date, explicit_end_date, str_start_date, str_explicit_end_date, year, operating_status, asset_type, output_folder):
        # Implement this function based on your requirement
        # Return a dictionary of API function calls
        pass

    #------------------------------------------------
    # Time-based Inputs
    #------------------------------------------------
    services = ['OLD_AESO', 'NEW_AESO']  # List your services here
    start_date_year = 2020
    number_of_years = 3
    end_date_year = 2022
    explicit_end_date = datetime.datetime(2023, 1, 1)
    sqlite_output = True
    remove_existing_output_files = True
    output_folder = 'C:/Users/User/output'
    #date_str = None 
    date_str = current_date.strftime('%Y-%m-%d')
    year = None
    operating_status = None
    asset_type = None
    #------------------------------------------------
    # CREATE API CALL DICTIONARY
    #------------------------------------------------
    for service in services:
        aeso_key, base_url, output_folder = get_api_credentials(service)
        api_function_call_dict = build_api_request_repository(api_activation_dict, aeso_key, base_url, start_date_year, end_date_year, explicit_end_date, str(start_date_year), str(explicit_end_date), None, None, None, output_folder)
        print(f"API Function Call Dictionary: {api_function_call_dict}")

        #------------------------------------------------
        # Create Instance of the API Client
        #------------------------------------------------
        api_client = APIClient(base_url)

        if remove_existing_output_files:
            remove_folder_contents(output_folder)
            print(f"Base output directory cleared: {output_folder}")
        #------------------------------------------------
        #Set-up SQLite Data Base
        #------------------------------------------------
        if sqlite_output:
            sub_folder_template = 'SQLite/'
            db_file_name = 'Alberta_Hourly_Merit_Order_Test_File.db'
            db_table_name = 'merit_order_daily_hourly_data'
            data_base_full_path = create_path(output_folder, sub_folder_template, db_file_name)
            conn = create_sqlite_table(data_base_full_path, db_table_name)
        else:
            conn = None

        try:
            for entity_key, entity_value in api_function_call_dict.items():
                for category_key, api_config in entity_value.items():
                    if 'output_consolidated_csv_files' not in api_config:
                        print(f"Missing 'output_consolidated_csv_files' in entity: {entity_key}, category: {category_key}")
                        continue

                    output_csv_files = api_config['output_csv_files']
                    function_name = api_config['function_name']
                    data_type = api_config['data_type']
                    sub_folder_template = api_config['sub_folder_template']
                    file_name_template = api_config['file_name_template']
                    column_order = api_config['column_order']
                    run_option = api_config['run_option']
                    consolidate_files = api_config['consolidate_files']
                    output_consolidated_csv_files = api_config['output_consolidated_csv_files']

                    if run_option:
                        print(f"Fetching data for {category_key}...")

                        try:
                            for year in range(start_date_year, start_date_year + number_of_years):
                                updated_start_date = f"{year}-01-01"
                                if year < end_date_year:
                                    updated_end_date = f"{year}-12-31"
                                else:
                                    updated_end_date = explicit_end_date.strftime('%Y-%m-%d')

                                endpoint = api_config['api_url']
                                params = api_config.get('params', {})
                                fetched_data = api_client.get(endpoint, params=params)

                                if fetched_data:
                                    post_process_function = getattr(utilities, function_name)
                                    year_str = str(year)
                                    updated_file_name_template = file_name_template.replace('None', year_str)
                                    path = create_path(output_folder, sub_folder_template, updated_file_name_template)

                                    processed_data_df = post_process_function(api_config, fetched_data, output_csv_files, pd.to_datetime(updated_start_date), pd.to_datetime(updated_end_date), explicit_end_date, year, path, True, sqlite_output, conn, db_table_name, column_order)
                                else:
                                    print(f"No data fetched for {category_key}")

                            if consolidate_files and fetched_data:
                                consolidate_annual_files(api_config, output_folder, output_consolidated_csv_files, sub_folder_template, True, sqlite_output, conn, db_table_name, column_order)

                        except Exception as e:
                            print(f"An error occurred while fetching data for {category_key}")
                            print(f"Error: {e}")

        except Exception as e:
            print(f"An error occurred with API calls for {service}")
            print(f"Error: {e}")
            
#########################################
# Call Main Function
if __name__ == "__main__":
    main()
    
