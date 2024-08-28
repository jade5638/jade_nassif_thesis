#%%
import os
import pandas as pd
import numpy as np
os.chdir('C:\\Users\\USER\\OneDrive - Cranfield University\\IRP\\optimisation_new')



database=pd.read_excel('database.xlsx',index_col=0)

def viscous_drag_estimate(Mach, Re_nb, Sref, Swet, Lref, version):
# 
# Function performs empirical estimation of the viscous drag based on geometry
# and flight conditions. It had two versions which differ in the estimate of the
# skin friction coefficient. The one used by Polito in Stratofly paper and another
# one from Raymer.
 
# Args:
# Mach (float): flight mach number
# Re_nb (float): Reynolds number
# Sref (float): reference area (would typically be projected area)
# Swet (float): wetted area of vehicle
# Lref (float): reference length of the vehicle, to be used in conjunction with Reynolds number
# version (string): type of estimate to be used, either "Stratofly" or "Raymer"
 
# Return:
# (float): the viscous drag
# 
 
    if version == "Stratofly":
        return 0.43*(1/np.log10(Lref*Re_nb)**2.58)*1/(1+0.31*Mach**2)**0.37*(Swet/Sref)
    
    if version == "Raymer":
        return 0.455*(1/np.log10(Lref*Re_nb)**2.58)*1/(1+0.144*Mach**2)**0.65 * (Swet/Sref)
    
database=pd.read_excel('database.xlsx',index_col=0)

ref_area=36 #m^2, average of the database s_ref

CD_M5=[]
CL_M5=[]
CD_M8=[]
CL_M8=[]

CD_visc_M5=[]
CD_visc_M8=[]

drag_visc_M5=[]
drag_visc_M8=[]

rho_M5=3.940e-2
rho_M8=1.797e-2

v_M5=1490.0
v_M8=2416

L=7 #meters
mu_M5=1.449e-5
mu_M8=1.476e-5

Re_M5=rho_M5*v_M5*L/mu_M5
Re_M8=rho_M8*v_M8*L/mu_M8

for i, point in database.iterrows():

    cd_M5=point["Drag_M5"]/(0.5*rho_M5*(v_M5**2)*ref_area)
    cd_M8=point["Drag_M8"]/(0.5*rho_M8*(v_M8**2)*ref_area)

    cl_M5=point["Lift_M5"]/(0.5*rho_M5*(v_M5**2)*ref_area)
    cl_M8=point["Lift_M8"]/(0.5*rho_M8*(v_M8**2)*ref_area)

    version='Stratofly'
    # version='Raymer'

    visc_m5=viscous_drag_estimate(Mach=5,Re_nb=Re_M5,Sref=ref_area,Swet=point['s_wet']/2,Lref=L,version=version)
    visc_m8=viscous_drag_estimate(Mach=8,Re_nb=Re_M8,Sref=ref_area,Swet=point['s_wet']/2,Lref=L,version=version)

    cd_visc_M5=cd_M5+visc_m5
    cd_visc_M8=cd_M8+visc_m8

    drag_visc_M5.append(cd_visc_M5*0.5*rho_M5*v_M5**2*ref_area)
    drag_visc_M8.append(cd_visc_M8*0.5*rho_M8*v_M8**2*ref_area)

    CD_M5.append(cd_M5)
    CD_M8.append(cd_M8)
    CL_M5.append(cl_M5)
    CL_M8.append(cl_M8)
    CD_visc_M5.append(cd_visc_M5)
    CD_visc_M8.append(cd_visc_M8)

database["CL_M5"]=CL_M5
database['CD_M5']=CD_M5
database["CL_M8"]=CL_M8
database['CD_M8']=CD_M8
database['CD_visc_M5']=CD_visc_M5
database['CD_visc_M8']=CD_visc_M8
database['Drag_visc_M5']=drag_visc_M5
database['Drag_visc_M8']=drag_visc_M8
database['LD_visc_M5']=database['CL_M5']/database['CD_visc_M5']
database['LD_visc_M8']=database['CL_M8']/database['CD_visc_M8']
database['%visc_M5']=(database['CD_visc_M5']-database['CD_M5'])/(database['CD_visc_M5'])*100
database['%visc_M8']=(database['CD_visc_M8']-database['CD_M8'])/(database['CD_visc_M8'])*100
database['delta_D_visc']=(database['Drag_visc_M8']-database['Drag_visc_M5'])/database['Drag_visc_M5']*100

# export updated database
database.to_excel('database.xlsx',index=True)



    

