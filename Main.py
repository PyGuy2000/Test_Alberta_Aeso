#from initializer import initialize_global_variables
import initializer as init # this is an alias for initializer
import global_variables as gv # this is an alias for global_variables
from global_variables import( 
    gbl_first_year_data,
    gbl_last_year_data,
    gbl_last_year_data_for_graphing,
    gbl_last_month_data,
    gbl_datetime_col_name,
    gbl_metadata_start_year_column_hdr,
    gbl_metadata_retirement_year_column_hdr,
    gbl_last_year_data_for_graphing,
    gbl_metadata_asset_id_column_hdr,
    gbl_datetime_col_name, 
    gbl_datetime_hourly_timeseries_format,
    gbl_metadata_asset_name_long_column_hdr,
    gbl_metadata_asset_name_column_hdr,
    gbl_metadata_repower_flag_column_hdr,
    gbl_metadata_prelinminary_status_column_hdr,
    gbl_metadata_status_check_column_hdr,
    gbl_metadata_status_column_hdr,
    gbl_metadata_fuel_type_column_hdr)

from Utilities import (
    setup_directories,
    insert_header_footer)

from config import(
    code_begin, 
    code_end,
    set_custom_rcparams,
    reset_rcparams_to_default,
    apply_custom_style_to_plotly,
    #tech type
    tech_type_desired_order, 
    tech_type_list_plus_BTF,
    original_tech_type_desired_order,
    tech_type_colors,
    tech_type_font_colors,
    tech_type_custom_line_thickness,
    tech_type_markers,
    tech_type_custom_line_styles,
    tech_type_desired_order_reduced,
    tech_type_reduced_colors,
    tech_type_font_colors,
    tech_type_custom_line_thickness_reduced,
    tech_type_reduced_custom_line_styles,
    #color pallette
    custom_color_palette,
    original_color_map,
    #fuel type
    fuel_type_desired_order,
    fuel_type_colors,
    original_fuel_type_color_map,
    fuel_type_font_colors,
    fuel_type_custom_line_thickness,
    fuel_type_markers,
    fuel_type_custom_line_styles
)

from input_data_prep import(   
    run_update_metered_volume,
    run_hourly_spot_power_data_prep,
    run_prep_generator_meta_data,
    run_prep_natural_gas_data,
    run_prep_on_demand_data,
    run_prep_on_production_data,
    run_clean_all_data,
    run_production_chart_final_prep,
    run_production_dict_convert_to_df
 )

from market_analysis import(
    run_calculate_production_emissions_by_tech_type,
    run_calculate_production_emmissions_by_time_frequency,
    run_calculate_production_emission_costs_by_time_frequency,
    run_aeso_metadata_search_and_updated,
    run_stats_on_meta_data,
    #run_technology_count_on_meta_data,
    run_stats_on_demand_data,
    run_avg_daily_load_by_Quarter_for_specfic_year,
    create_demand_visualizations,
    create_interactive_hourly_demand_visualizations,
    run_load_factor_and_demand_duration_analysis,
    run_power_generation_location_data,
    run_transmission_and_substation_map,
    run_load_capacity_data_from_meta_data,
    run_process_capacity_additions_retirements,
    run_reserve_margin_analysis,
    run_hourly_production_by_asset_id,
    run_comparative_hourly_production_by_tech_type_for_range_of_years,
    run_average_daily_production_by_quarter_for_specific_year,
    run_annual_production_by_technology_type_over_time,
    run_create_production_pie_charts_by_tech_type,
    run_hourly_production_by_tech_type,
    run_production_historgram_specific_asset,
    run_comparative_production_by_asset,
    run_comparative_proudction_by_specific_tech_type,
    run_production_by_tech_type_heatmap,
    run_calculate_inferred_outages,
    run_inferred_starts_and_stops,
    #run_capacity_factor_and_demand_duration_analysis,
    capacity_factor_analysis,
    #capacity_factor_calculations_by_asset_and_technology_type,
    capacity_factor_by_tech_type_time_series,
    violin_graph_for_capacity_factor_time_series_by_tech_type,
    capacity_factor_heat_map,
    capacity_factor_by_asset_for_a_given_year,
    capacity_factor_by_asset_for_a_given_year_grouped_by_technology_type,
    hourly_spot_price_frequency_analysis,
    compute_daily_on_off_peak_spread_for_spot_power_prices,
    spot_price_static_time_series_charts,
    #spot_price_dynamic_time_series_charts,
    create_hourly_duration_curves_by_year,
    perecent_revenue_earned_in_each_year_by_percent_hours_in_year,
    #calculate_difference_between_spot_price_and_forecast,
    statistical_analysis_by_year_for_spot_power_prices,
    case_study_ndp_control_of_ppa_terminating_assets,
    pool_price_volatility_and_wind_intermittency,
    natural_gas_analysis,
    natural_gas_static_spot_prices,
    hourly_spot_natural_gas_duration_curves_by_year,
    market_heat_rate_volatility,
    calculate_hourly_and_annual_revenue_by_asset_id,
    calculate_hourly_and_annual_revenue_by_tech_types,
    stacked_area_graphs_for_revenue_by_tech_type,
    calculate_received_spot_prices_hourly_monthly_and_annually_by_asset_and_tech_type,
    create_histogram_for_multiple_assets_multiple_years,
    create_histograms_for_tech_type_received_spot_prices,
    calculate_and_graph_received_spot_for_select_assets_and_years,
    calculate_and_graph_received_spot_for_select_assets_and_years,
    calculate_and_graph_received_spot_for_select_tech_types_and_years,
    graph_spot_as_ratio_to_average_spot_by_all_tech_types,
    calculate_and_graph_received_spot_with_confidence_intervals,
    back_casted_capacity_factor_example,
    merit_order_data_analysis,
    merit_order_daily_hour_graph
)


#------------------------------------------------
# PARTN A:  Initialize global variables and set up directories
#------------------------------------------------
# Define file paths both input and output files
#ide_option, base_output_directory_global, base_input_directory_global, output_dir, input_dir, csv_folder, image_folder = initialize_global_variables('vscode')  # Set this based on your environment vscode/kaggle/jupyter_notebook
init.initialize_global_variables('vscode') 
# Setup global variables that depend on initialization and file paths from the previous step
# to load input files
#gv.setup_global_variables(ide_option,  base_input_directory_global, input_dir)
#gv.setup_global_variables(base_input_directory_global, input_dir)
gv.setup_global_variables()

print(
    gbl_metadata_asset_id_column_hdr,
    gbl_metadata_asset_name_long_column_hdr,
    gbl_metadata_asset_name_column_hdr,
    gbl_metadata_repower_flag_column_hdr,
    gbl_metadata_prelinminary_status_column_hdr,
    gbl_metadata_status_check_column_hdr,
    gbl_metadata_status_column_hdr,
    gbl_metadata_fuel_type_column_hdr)

assert gv.gbl_existing_production_df is not None, "gbl_existing_production_df is not initialized properly"

# Delete existing output files in output folder and create csv and image folders
# This only relates to the output files not the input files
# setup_directories(base_output_directory_global)

# Step 1: Setup Directories
setup_directories()
print("Step 0: Directories Setup completed")

#------------------------------------------------
# PART B: Prepare and Clean Data for Analysis
#------------------------------------------------
# Step 1 Update Metered Volume Data
# Combine existing and updated metered volume files based on file paths from above
insert_header_footer("Step 1: Updated Metered Volume Data",1) 
run_update_metered_volume()
print("Step 1: Updated Metered Volume Data completed")

# Step 2: # Prep Generator Meta Data and Obtain Early Count of Technology Types from Meta Data
insert_header_footer("Step 2: Prepped Generator Meta Data ",1) 
run_prep_generator_meta_data()
print("Step 2: Prepped Generator Meta Data completed")

# Step 3: # Convert Daily Natural Gas Prices to Hourly
insert_header_footer("Step 3: Prepped Natural Gas Data",1) 
run_prep_natural_gas_data()
print("Step 3: Prepped Natural Gas Data completed")

# Step 4: # Concatenate Pool Price Data 
insert_header_footer("Step 4: Prepped Pool Price Data ",1) 
run_hourly_spot_power_data_prep()
print("Step 4: Prepped Pool Price Data completed")

# Step 5 Concatenate Demand Data
insert_header_footer("Step 5: Prepped Demand Data",1) 
run_prep_on_demand_data()
print("Step 5: Prepped Demand Data completed")

# Step 6 Concatenate Production Data
insert_header_footer("Step 6: Prepped Production Data",1) 
run_prep_on_production_data()
print("Step 6: Prepped Production Data completed")

# Step 7 Align Data for Cleaning
insert_header_footer("Step 7: Cleaned Data",1) 
run_clean_all_data()
print("Step 7: Cleaned Data completed")


#------------------------------------------------
# PART B: Post-Processing Data for Analysis
#------------------------------------------------

# Step 7: # Create Annual, Monthly and Hourly Production Data by Asset Type and Technology Type
# Note this creates a list of dictionaries for each year - this will be coverted to data frames
# in the next step
insert_header_footer("Step 7: Updated Metered Volume Data",1) 
run_production_chart_final_prep()

# Step 8: Convert production dictinoaries to data frames
insert_header_footer("Step 8: Updated Metered Volume Data",1) 
run_production_dict_convert_to_df()

#------------------------------------------------
# PART C: Master Analysis
#------------------------------------------------

#................................................
# Production Emissions
#................................................
# Step 9: Calculated Emissions
insert_header_footer("Step 1: Updated Metered Volume Data",1) 
run_calculate_production_emmissions_by_time_frequency()

# Step 10: Calculated Emissions by Technology Type
insert_header_footer("Step 1: Updated Metered Volume Data",1) 
run_calculate_production_emissions_by_tech_type()


# Step 11: Production Emissions Costs by Time Frequency by Asset Type and Technology Type
insert_header_footer("Step 1: Updated Metered Volume Data",1) 
run_calculate_production_emission_costs_by_time_frequency()

#................................................
# Calibrate Asset Data with AESO Data
#................................................
# Step 12: Search AESO Website for Missing Meta Data on ASSET_IDs in Previous Section of Code
insert_header_footer("Step 1: Updated Metered Volume Data",1) 
aeso_df = run_aeso_metadata_search_and_updated()

#................................................
#GPS Coorindate Generator for Development Projects
#................................................

#................................................
# Step 13: Run Stats on Meta Data
#................................................
insert_header_footer("Step 1: Updated Metered Volume Data",1) 
run_technology_count_on_meta_data()

#................................................
# Step 14: Demand and Load Data
#................................................
insert_header_footer("Step 14.1: Updated Metered Volume Data",1) 
run_stats_on_demand_data()

#run_avg_daily_load_by_Quarter_for_specfic_year()
insert_header_footer("Step 14.2: Updated Metered Volume Data",1) 
create_demand_visualizations()

insert_header_footer("Step 14.3: Updated Metered Volume Data",1) 
create_interactive_hourly_demand_visualizations()

insert_header_footer("Step 14.4: Updated Metered Volume Data",1) 
run_load_factor_and_demand_duration_analysis()

#................................................
# Step 15: Power Generation Capacity, Production and Geospatial Data
#................................................
graph_year = 2024
planning_areas_gdf = run_power_generation_location_data()
insert_header_footer("Step 15.1: Updated Metered Volume Data",1) 
run_transmission_and_substation_map()

insert_header_footer("Step 15.2: Updated Metered Volume Data",1) 
run_load_capacity_data_from_meta_data()
#run_comapartive_capacity_splits_by_year()
insert_header_footer("Step 15.3: Updated Metered Volume Data",1) 
run_process_capacity_additions_retirements()

#________________________________________________
# Step 16: Reserve Margin Analysis
#________________________________________________
insert_header_footer("Step 16: Updated Metered Volume Data",1) 
run_reserve_margin_analysis()
#________________________________________________
# Step 17: Production Analysis
#________________________________________________
insert_header_footer("Step 17.1: Updated Metered Volume Data",1) 
run_hourly_production_by_asset_id()

insert_header_footer("Step 17.2: Updated Metered Volume Data",1) 
run_comparative_hourly_production_by_tech_type_for_range_of_years()

insert_header_footer("Step 17.3: Updated Metered Volume Data",1) 
run_average_daily_production_by_quarter_for_specific_year()

insert_header_footer("Step 17.4: Updated Metered Volume Data",1) 
run_annual_production_by_technology_type_over_time()

insert_header_footer("Step 17.5 Updated Metered Volume Data",1) 
run_create_production_pie_charts_by_tech_type()

insert_header_footer("Step 17.6: Updated Metered Volume Data",1) 
run_hourly_production_by_tech_type()

insert_header_footer("Step 17.7: Updated Metered Volume Data",1) 
run_production_historgram_specific_asset()

insert_header_footer("Step 17.8: Updated Metered Volume Data",1) 
run_comparative_production_by_asset()

insert_header_footer("Step 17.9: Updated Metered Volume Data",1) 
run_comparative_proudction_by_specific_tech_type()

insert_header_footer("Step 17.10: Updated Metered Volume Data",1) 
run_production_by_tech_type_heatmap()

#________________________________________________
# Step 18: Outage Analysis
#_______________________________________________
insert_header_footer("Step 18.1: Updated Metered Volume Data",1) 
run_calculate_inferred_outages()

insert_header_footer("Step 18.2: Updated Metered Volume Data",1) 
run_inferred_starts_and_stops()
#run_number_of_starts_per_MW_by_tech_type()

#________________________________________________
# Step 19: Capacity Factor Analysis
#_______________________________________________
insert_header_footer("Step 19.1: Updated Metered Volume Data",1) 
capacity_factor_analysis()

# Annual_formatted_capacity_factors_by_asset, annual_formatted_capacity_factors_by_tech, max_capacity_by_tech_df, annual_capacity_factors_percent_by_tech = \
#     capacity_factor_calculations_by_asset_and_technology_type()
insert_header_footer("Step 19.2: Updated Metered Volume Data",1) 
capacity_factor_by_tech_type_time_series()

insert_header_footer("Step 19.3: Updated Metered Volume Data",1) 
violin_graph_for_capacity_factor_time_series_by_tech_type()

insert_header_footer("Step 19.4: Updated Metered Volume Data",1) 
capacity_factor_heat_map()

insert_header_footer("Step 19.5: Updated Metered Volume Data",1) 
capacity_factor_by_asset_for_a_given_year()

insert_header_footer("Step 19.6: Updated Metered Volume Data",1) 
capacity_factor_by_asset_for_a_given_year_grouped_by_technology_type()


#________________________________________________
# Step 20: Spot Power Analysis
#_______________________________________________
insert_header_footer("Step 20.1: Updated Metered Volume Data",1) 
hourly_spot_price_frequency_analysis()

insert_header_footer("Step 20.2: Updated Metered Volume Data",1) 
compute_daily_on_off_peak_spread_for_spot_power_prices()

insert_header_footer("Step 20.3: Updated Metered Volume Data",1) 
spot_price_static_time_series_charts()

#spot_price_dynamic_time_series_charts()

# Define the list of years you want to include
years = [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021,  2022, 2023]  # example years
insert_header_footer("Step 20.4: Updated Metered Volume Data",1) 
create_hourly_duration_curves_by_year()

#________________________________________________
# Step 21: Revenue Analysis
#_______________________________________________
insert_header_footer("Step 21.1: Updated Metered Volume Data",1) 
perecent_revenue_earned_in_each_year_by_percent_hours_in_year()

#calc
insert_header_footer("Step 21.2: Updated Metered Volume Data",1) 
statistical_analysis_by_year_for_spot_power_prices()

insert_header_footer("Step 21.3: Updated Metered Volume Data",1) 
case_study_ndp_control_of_ppa_terminating_assets()

insert_header_footer("Step 21.4: Updated Metered Volume Data",1) 
pool_price_volatility_and_wind_intermittency()

#________________________________________________
# Step 22: Natural Gas Analysis
#_______________________________________________
insert_header_footer("Step 22.1: Updated Metered Volume Data",1) 
natural_gas_analysis()

insert_header_footer("Step 22.2: Updated Metered Volume Data",1) 
natural_gas_static_spot_prices()

insert_header_footer("Step 22.3: Updated Metered Volume Data",1) 
hourly_spot_natural_gas_duration_curves_by_year()

#________________________________________________
# Step 23: Market Heat Rate Volatility
#_______________________________________________
insert_header_footer("Step 23: Updated Metered Volume Data",1) 
market_heat_rate_volatility()

#________________________________________________
# Step 24: Revenue and Recieved Spot Prices Analysis
#_______________________________________________
insert_header_footer("Step 24.1: Updated Metered Volume Data",1) 
calculate_hourly_and_annual_revenue_by_asset_id()

insert_header_footer("Step 24.2: Updated Metered Volume Data",1) 
calculate_hourly_and_annual_revenue_by_tech_types()

insert_header_footer("Step 24.3: Updated Metered Volume Data",1) 
stacked_area_graphs_for_revenue_by_tech_type()

insert_header_footer("Step 24.4: Updated Metered Volume Data",1) 
calculate_received_spot_prices_hourly,_monthly_and_annually_by_asset_and_tech_type()

insert_header_footer("Step 24.5: Updated Metered Volume Data",1) 
create_histograms_for_tech_type_received_spot_prices()

insert_header_footer("Step 24.6: Updated Metered Volume Data",1) 
create_histogram_for_multiple_assets_multiple_years()

insert_header_footer("Step 24.7: Updated Metered Volume Data",1) 
calculate_and_graph_received_spot_for_select_assets_and_years()

insert_header_footer("Step 24.8: Updated Metered Volume Data",1) 
calculate_and_graph_received_spot_for_select_tech_types_and_years()

insert_header_footer("Step 24.9: Updated Metered Volume Data",1) 
graph_spot_as_ratio_to_average_spot_by_all_tech_types()

insert_header_footer("Step 24.10: Updated Metered Volume Data",1) 
calculate_and_graph_received_spot_with_confidence_intervals()

#________________________________________________
# Step 25: Backcasted Capacity Factor Example
#_______________________________________________
year_list = [2010,2011,2012,2013,2014,2015,2016,2017,2018,2019,2020,2021,2022,2023] 
insert_header_footer("Step 25: Updated Metered Volume Data",1) 
back_casted_capacity_factor_example()

#________________________________________________
# Step 26: Merit Order Data Analysis
#_______________________________________________
# Create query variable for specific asset id
year = 2023
asset_id_example = 'HRM'
tech_type_example = 'COMBINED_CYCLE'
insert_header_footer("Step 26.1: Updated Metered Volume Data",1) 
merit_order_data_analysis()

insert_header_footer("Step 26.2: Updated Metered Volume Data",1) 
merit_order_daily_hour_graph()
