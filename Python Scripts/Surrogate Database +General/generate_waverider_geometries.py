#%%
import os
import sys
os.chdir('C:\\Users\\USER\\OneDrive - Cranfield University\\IRP\\optimisation_new\\Geometries')
sys.path.append("../")
from waverider_generator.generator import waverider as wr
from waverider_generator.cad_export import to_CAD
import numpy as np
import pandas as pd
from setup import setup
import pickle
# assuming local directory is the Geometries folder 

final_sample_points=np.array(pd.read_excel("../database.xlsx",index_col=0))

setup_variables=setup()

# parameters
height=setup_variables['height']
width=setup_variables['width']
beta=setup_variables['beta']
n=setup_variables['n']


#%%
waveriders={}

for i,sample in enumerate(final_sample_points):

    waverider=wr(M_inf=sample[0],
                 beta=beta,
                 height=height,
                 width=width,
                 dp=list(sample[1:]),
                 n_upper_surface=10000,
                 n_shockwave=10000,
                 n_planes=30,
                 n_streamwise=30,
                 delta_streamwise=0.1)
    print(f"{i+1} of {n}")
    waveriders[f'waverider_{i+1}']=waverider

    # scale =1000 to get meters
    to_CAD(waverider=waverider,sides='both',export=True,filename=f'waverider_{i+1}.step',scale=1000)

# waveriders.pkl used in get_projected_surface.py
with open("../waveriders.pkl","wb") as f:
    pickle.dump(waveriders,f)