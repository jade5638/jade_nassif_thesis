import os
import glob

# define the extension you want to delete
extension = ".sim~"

def clean_folder(min_or_max: str):
    # get current directory
    os.chdir(f'C:\\Users\\USER\\OneDrive - Cranfield University\\IRP\\optimisation_new\\{min_or_max}_setup')

    cd=os.getcwd()

    # find all files with the given extension
    files_to_delete = glob.glob(f"{cd}/*{extension}")

    # delete each file
    for file in files_to_delete:
        os.remove(file)
        print(f"Deleted: {file}")

    print("complete")

clean_folder('min')
clean_folder('max')