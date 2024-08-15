#from Utilities import convert_to_function_name

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

# Convert strinng to function name
strings = [
    "Capacity Factor Analysis",
    "Capacity Factor Calculations by Asset and Technology Type",
    "Capacity Factor by Tech Type Time Series",
    "Violin Graph for Capacity Factor Time Series by Tech Type",
    "Capacity Factor Heat Map",
    "Capacity Factor by Asset for a Given Year",
    "Capacity Factor by Asset for a Given Year Grouped by Technology Type",
    "Hourly Spot Price Frequency Analysis",
    "Compute Daily On/Off-Peak Spread for Spot Power Prices",
    "Spot Price Static Time Series Charts",
    "Spot Price Dynamic Time Series Charts",
    "Create Hourly Duration Curves by Year",
    "Perecent Revenue Earned in Each Year by Percent Hours in Year",
    "Calculate Difference Between Spot Price and Forecast",
    "Statistical Analysis by Year for Spot Power Prices",
    "Case Study: NDP Control of PPA-terminating Assets*",
    "Pool Price Volatility and Wind Intermittency",
    "Natural Gas Analysis",
    "Natural Gas Static Spot Prices",
    "Hourly Spot Natural Gas Duration Curves by Year",
    "Market Heat Rate Volatility",
    "Calculate Hourly and Annual Revenue by Asset ID",
    "Calculate Hourly and Annual Revenue by Tech Types",
    "Stacked Area Graphs for Revenue by Tech Type",
    "Calculate Received Spot Prices Hourly, Monthly and Annually by Asset and Tech Type",
    "Create Histograms for TECH_TYPE Received Spot Prices",
    "Calculate and Graph Received Spot for Select Assets and Years*",
    "Calculate and Graph Received Spot for Select Assets and Years*",
    "Calculate and Graph Received Spot for Select Tech Types and Years",
    "Graph Spot As Ratio To Average Spot by ALL Tech Types",
    "Calculate and Graph Received Spot with Confidence Intervals",
    "Back-casted Capacity Factor Example",
    "Merit Order Data Analysis"
]

function_names = [convert_to_function_name(s) for s in strings]

for func_name in function_names:
    print(func_name)