import os
import shutil
import sys
excluded_extensions = ['.sim','sim~'] 

#this code simply moved all log files from the main results folder to the logs folder. 
def rename_logs(min_or_max):

    cd=f'C:\\Users\\USER\\OneDrive - Cranfield University\\IRP\\optimisation_new\\result_files\\{min_or_max}\\logs'
    os.chdir(cd)

    source=cd

    for filename in os.listdir(source):
        # file_path=os.path.join(destination,filename)

        root, ext = os.path.splitext(filename)
        if ext!='.txt':
            new_filename = root + ".txt"

            os.rename(filename,new_filename)
            print(f'Renamed: {filename} to {new_filename}')


rename_logs('min')
rename_logs("max")
