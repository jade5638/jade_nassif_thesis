import re
import os
from setup import setup
import sys
setup_variables=setup()
n=setup_variables['n']

# this script makes use of patterns in the base_setup_max.java and base_setup_min.java files to automate the process of creating
# macros and subs for all waverider simulations
def generate_macros(min_or_max):

    os.chdir(f"C:\\Users\\USER\\OneDrive - Cranfield University\\IRP\optimisation_new\\Macros\\{min_or_max}")
    sys.path.append("..//..//")
    
    with open(os.path.join('..//..//',f'base_setup_{min_or_max}.java'), 'r') as file:
        original_macro = file.read()

   
    pattern1= re.compile(r'String waverider_name="waverider";')
    pattern2= re.compile(r'String save_filename="waverider";')
    pattern3=re.compile(f'public class base_setup_{min_or_max}')
    for i in range(1,n+1):

        modified_macro=original_macro

        replacement1=f'String waverider_name="waverider_{i}";'
        replacement2=f'String save_filename="waverider_{i}_{min_or_max}";'
        replacement3=f'public class waverider_{i}_{min_or_max}'
        replacements = {
                pattern1 : replacement1,
                pattern2: replacement2,
                pattern3: replacement3
        }
        for pattern, replacement in replacements.items():
            modified_macro = re.sub(pattern, replacement, modified_macro)

        with open(f'waverider_{i}_{min_or_max}.java', 'w') as file:
            file.write(modified_macro)

def generate_subs(min_or_max):

    os.chdir(f"C:\\Users\\USER\\OneDrive - Cranfield University\\IRP\optimisation_new\\sub_files\\{min_or_max}")
    sys.path.append("..//..//")

    with open(os.path.join('..//..//','starccm.sub'), 'r') as file:
        original_sub = file.read()
    
    pattern1=re.compile(r'#PBS -N waverider')
    pattern2=re.compile(r'-rsh ssh waverider.sim')

    for i in range(1,n+1):

        modified_sub=original_sub

        replacement1=f'#PBS -N waverider_{i}_{min_or_max}'
        replacement2=f'-rsh ssh waverider_{i}_{min_or_max}.sim'
        replacements = {
                pattern1 : replacement1,
                pattern2: replacement2
        }
        for pattern, replacement in replacements.items():
            modified_sub = re.sub(pattern, replacement, modified_sub)

        with open(f'waverider_{i}_{min_or_max}.sub', 'w',newline='\n') as file:
            file.write(modified_sub)


generate_macros('min')
generate_macros('max')

generate_subs('min')
generate_subs('max')


