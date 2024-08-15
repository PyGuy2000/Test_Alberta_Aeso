import pandas as pd
import os
import re

# get all csv files in the specified directory
folder_path = r'C:\Users\kaczanor\OneDrive - Enbridge Inc\Documents\Python\AB Electricity Sector Stats\output_data\CSV_Folder'
files = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.endswith('.csv')]

# extract year from file name
def get_year(file_name):
    match = re.search('\d{4}', file_name)
    return int(match[0]) if match else 0

# sort files in descending order
files.sort(key=get_year, reverse=True)

# read the first file
df = pd.read_csv(files[0], index_col=0)
year = get_year(files[0])
if 'Capacity_Factor' in df.columns:
    df = df.rename(columns={'Capacity_Factor': str(year)})

# loop through the rest of the files
for file in files[1:]:
    temp_df = pd.read_csv(file, index_col=0)
    year = get_year(file)
    if 'Capacity_Factor' in temp_df.columns:
        temp_df = temp_df.rename(columns={'Capacity_Factor': str(year)})
    if 'Tech_Type' in temp_df.columns and 'Asset_ID' in temp_df.columns:
        df = pd.merge(df, temp_df, how='outer', on=['Tech_Type', 'Asset_ID'])

df = df.sort_values(['Tech_Type', 'Asset_ID'])
df.to_csv(os.path.join(folder_path, 'combined.csv'), index=False)