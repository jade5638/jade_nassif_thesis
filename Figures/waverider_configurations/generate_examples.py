
#%%
from waverider_generator.generator import waverider as wr
from waverider_generator.cad_export import to_CAD
import os
import pandas as pd
import numpy as np

os.chdir(f'C:\\Users\\USER\\OneDrive - Cranfield University\\IRP\\Figures\\waverider_configurations')

#this code is used to generate the various configurations which will be shown in the thesis report as examples
height=1.876
width=4.2
beta=15
M_inf=6.5
selected_waveriders_database=pd.read_excel('selected.xlsx',index_col=0)


for i,selected_combination in selected_waveriders_database.iterrows():

    dp=list(selected_combination[["X1","X2","X3","X4"]])
    
    waverider=wr(M_inf=M_inf,
                 beta=beta,
                 height=height,
                 width=width,
                 dp=dp,
                 n_upper_surface=10000,
                 n_shockwave=10000,
                 n_planes=30,
                 n_streamwise=30,
                 delta_streamwise=0.1)
    
    to_CAD(waverider=waverider,sides='both',export=True,filename=f'waverider_{i}.step',scale=1000)

