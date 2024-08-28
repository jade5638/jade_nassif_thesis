# This code extracts the lift and drag from the last line in the logs
#%%
import os
import pandas as pd

os.chdir(f'C:\\Users\\USER\\OneDrive - Cranfield University\\IRP\\optimisation_new')
         
database=pd.read_excel('database.xlsx',index_col=0)

def extract_lift_drag(min_or_max: str):

    os.chdir(f'C:\\Users\\USER\\OneDrive - Cranfield University\\IRP\\optimisation_new\\result_files\\{min_or_max}\\logs')
    
    global database

    Lift=[]
    Drag=[]
    LD=[]
    for i in database.index:

        with open(f'waverider_{i}_{min_or_max}.txt','r') as log:
            lines=log.readlines()
            n_lines=len(lines)
            target_line=n_lines-5

            # reads the lift drag and ld from documents. their positions are 6 7 and 8 always. (found by trial and error)
            last_line=lines[target_line].strip()
            values=last_line.split()
            drag=float(values[6])
            lift=float(values[8])
            ld=float(values[7])

            LD.append(ld)
            Drag.append(drag)
            Lift.append(lift) 
    
    return Drag,Lift,LD


Drag_max,Lift_max,LD_max=extract_lift_drag('max')
Drag_min,Lift_min,LD_min=extract_lift_drag('min')

database['Lift_M5']=Lift_min
database['Drag_M5']=Drag_min
database['Lift_M8']=Lift_max
database['Drag_M8']=Drag_max
database['LD_M8']=LD_max
database['LD_M5']=LD_min

os.chdir(f'C:\\Users\\USER\\OneDrive - Cranfield University\\IRP\\optimisation_new')
database.to_excel('database.xlsx',index=True)