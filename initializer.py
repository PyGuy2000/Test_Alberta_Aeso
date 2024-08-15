# initializer.py

import os


#Setup Directories
gbl_csv_folder = 'CSV_Folder'
gbl_image_folder = 'Image_Folder'
gbl_home_dir = 'C:/Users/Rob_Kaz/OneDrive/Documents/Rob Personal Documents/Python/AB Electricity Sector Stats'
gbl_office_dir = 'C:/Users/kaczanor/OneDrive - Enbridge Inc/Documents/Python/AB Electricity Sector Stats'

gbl_ide_option = None
gbl_base_output_directory_global = None
gbl_base_input_directory_global = None

def initialize_global_variables(ide_option):
    global gbl_ide_option, gbl_base_output_directory_global, gbl_base_input_directory_global, gbl_input_dir
    
    gbl_ide_option = ide_option
    
    if gbl_ide_option == 'vscode':
        if os.path.exists(gbl_home_dir):
            gbl_root_dir = gbl_home_dir
        else:
            gbl_root_dir = gbl_office_dir
        gbl_output_dir = "output_data/"
        gbl_input_dir = "input_data"  # removed the leading "/"
    elif gbl_ide_option == 'kaggle':
        gbl_root_dir = ''
        gbl_output_dir = '/kaggle/working/CSV_Folder'  # retained the leading "/"
        gbl_input_dir = '/kaggle/input/'  # retained the leading "/"

    elif gbl_ide_option == 'jupyter_notebook':
        gbl_root_dir = 'C:/Users/kaczanor/AB Electricity Sector Stats'
        gbl_output_dir = 'NA'
        gbl_input_dir = 'NA'

    gbl_base_output_directory_global = os.path.normpath(os.path.join(gbl_root_dir, gbl_output_dir))
    gbl_base_input_directory_global = os.path.normpath(os.path.join(gbl_root_dir, gbl_input_dir))
    
    print(f"{gbl_ide_option} base_output_directory_global set: {gbl_base_output_directory_global}")
    print(f"{gbl_ide_option} base_input_directory_global set: {gbl_base_input_directory_global}")
    
    #return gbl_ide_option, gbl_base_output_directory_global, gbl_base_input_directory_global, gbl_output_dir, gbl_input_dir,  gbl_csv_folder, gbl_image_folder
    return 