#%%
import pickle
import os
import pandas as pd
import numpy as np

os.chdir('C:\\Users\\USER\\OneDrive - Cranfield University\\IRP\\optimisation_new')

with open("waveriders.pkl",'rb') as f:
    waveriders=pickle.load(f)

database=pd.read_excel('database.xlsx',index_col=0)
projected_areas=[]
for i in database.index:

    waverider=waveriders[f'waverider_{i}']

    leading_edge=waverider.leading_edge

    leading_edge[:,0]= -leading_edge[:,0]+waverider.length

    area=abs(np.trapz(leading_edge[:,2],leading_edge[:,0]))

    projected_areas.append(2*area)

database["s_ref"]=projected_areas

database.to_excel('database.xlsx',index=True)


