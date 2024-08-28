from waverider_generator.generator import waverider as wr
from waverider_generator.cad_export import to_CAD
import os
import sys
os.chdir('C:\\Users\\USER\\OneDrive - Cranfield University\\IRP\\optimisation_new\\GCS')
sys.path.append("../")
from setup import setup
setup_variables=setup()
# parameters
height=setup_variables['height']
width=setup_variables['width']
beta=setup_variables['beta']
waverider=wr(M_inf=6.5,
                 beta=beta,
                 height=height,
                 width=width,
                 dp=[0.25,0.5,0.5,0.5],
                 n_upper_surface=10000,
                 n_shockwave=10000,
                 n_planes=30,
                 n_streamwise=30,
                 delta_streamwise=0.1)

to_CAD(waverider=waverider,sides='both',export=True,filename=f'waverider_GCS.step',scale=1000)