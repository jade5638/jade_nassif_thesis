#%%
import cadquery as cq
from cadquery import importers
import os
import pandas as pd
import numpy as np
os.chdir('C:\\Users\\USER\\OneDrive - Cranfield University\\IRP\\optimisation_new\\Geometries')

#This code is used to obtain the volume and projected surface areas of the sample geometries
# for more comments on process, see the file with the same name in Longitudinal Analysis folder
volumes=[]
s_wet=[]
cgs=[]
database=pd.read_excel(os.path.join('..','database.xlsx'),index_col=0)

for i in database.index:

    solid = importers.importStep(f'waverider_{i}.step')

    volumes.append(solid.val().Volume()*1e-9)
    
    faces = solid.val().Faces()
    face_areas = [face.Area() for face in faces]
    #case where we have 6 faces so back is in two parts in CAD
    if len(face_areas)==6:

        smallest_face_area = 2*min(face_areas)
    # case where back is one face
    elif len(face_areas)==5:

        smallest_face_area = min(face_areas)

    cg=solid.val().centerOfMass(solid.val())
    cgs.append(np.array(cg.toTuple())*1e-3)
    # append wetted surface minus back (the smallest)
    s_wet.append((solid.val().Area() - smallest_face_area)*1e-6)

database['Volume']=volumes
database["s_wet"]=s_wet
database["v_eff"]=np.array(volumes)**(2/3)/(np.array(s_wet)) 
database["cg_x"]=[cg[0] for cg in cgs]
database["cg_y"]=[cg[1] for cg in cgs]
database.to_excel(os.path.join('..','database.xlsx'),index=True)




