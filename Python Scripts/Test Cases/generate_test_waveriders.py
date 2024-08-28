
#%%
import os
os.chdir('C:\\Users\\USER\\OneDrive - Cranfield University\\IRP\\optimisation_new\\test_cases')
import sys
sys.path.append('../')
from waverider_generator.generator import waverider as wr
from waverider_generator.cad_export import to_CAD
from waverider_generator.plotting_tools import Plot_Base_Plane
from setup import setup
import matplotlib.pyplot as plt

setup_variables=setup()

# parameters
height=setup_variables['height']
width=setup_variables['width']
beta=setup_variables['beta']

'''
OPT1: max volume, max drag
OPT2: min volume, min drag, min lift
OPT3: max lift
'''
M_design_opt1=8
dp_opt1=[0.026,	1,	0,	0]

M_design_opt2=5
dp_opt2=[0,0,1,1]

M_design_opt3=8
# obtained as mean of the 5 runs
dp_opt3=[0.3570,0.4154,0,0]

M_designs=[M_design_opt1,M_design_opt2,M_design_opt3]
dps=[dp_opt1,dp_opt2,dp_opt3]
filenames=['waverider_opt1.step','waverider_opt2.step','waverider_opt3.step']
#%%
figs=[]
for M_design,dp,filename in zip(M_designs,dps,filenames):
    waverider=wr(M_inf=M_design,
                 beta=beta,
                 height=height,
                 width=width,
                 dp=dp,
                 n_upper_surface=10000,
                 n_shockwave=10000,
                 n_planes=30,
                 n_streamwise=30,
                 delta_streamwise=0.05)
    # to_CAD(waverider=waverider,sides='both',export=False,filename=filename,scale=1000)
    figs.append(Plot_Base_Plane(waverider=waverider,latex=True))

plt.show()