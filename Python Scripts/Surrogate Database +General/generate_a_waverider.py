
#%%
import os
os.chdir('C:\\Users\\USER\\OneDrive - Cranfield University\\IRP\\optimisation_new')

from waverider_generator.generator import waverider as wr
from waverider_generator.cad_export import to_CAD
from setup import setup


setup_variables=setup()

# parameters
M_design=7.98707922
height=setup_variables['height']
width=setup_variables['width']
beta=setup_variables['beta']
dp=[0.36889495,	0.38875234,	0,	0]
#%%
filename='waverider.step'
waverider=wr(M_inf=M_design,
                 beta=beta,
                 height=height,
                 width=width,
                 dp=dp,
                 n_upper_surface=10000,
                 n_shockwave=10000,
                 n_planes=30,
                 n_streamwise=30,
                 delta_streamwise=0.1)

to_CAD(waverider=waverider,sides='both',export=False,filename=filename,scale=1000)
