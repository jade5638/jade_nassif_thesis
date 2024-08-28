#%%
import cadquery as cq
from cadquery import importers
import os
import pandas as pd
import numpy as np
os.chdir('C:\\Users\\USER\\OneDrive - Cranfield University\\IRP\\optimisation_new\\Stability Analysis\\Geometries')

# import the stability database
stability_database=pd.read_excel('../stability_database.xlsx',index_col=0)

# initisalise lists containing volume s_wet and CG
volumes=[]
s_wet=[]
cgs=[]

# number of geometries n
n=10
for i in range(2,n+1):

    # import waverider step file
    solid = importers.importStep(f'waverider_{i}.step')

    # append volume. times 1e-9 because dimensions are in mm so to get meters^3 
    volumes.append(solid.val().Volume()*1e-9)
    
    # extract all faces and get areas
    faces = solid.val().Faces()
    face_areas = [face.Area() for face in faces]

    #in most cases, we have 5 faces (back, lower surface x2 upper surface x2)
    # however, sometimes the CAD export counts the back as two faces so we have 6 faces instead
    if len(face_areas)==6:

        # back is the smallest area always
        smallest_face_area = 2*min(face_areas)

    # case where back is one face
    elif len(face_areas)==5:

        smallest_face_area = min(face_areas)

    # find centre of mass
    cg=solid.val().centerOfMass(solid.val())

    cgs.append(np.array(cg.toTuple())*1e-3)

    # append wetted surface minus back
    s_wet.append((solid.val().Area() - smallest_face_area)*1e-6)

# populate columns

stability_database['Volume']=volumes
stability_database["s_wet"]=s_wet
stability_database["v_eff"]=np.array(volumes)**(2/3)/(np.array(s_wet))
stability_database["cg_x"]=[cg[0] for cg in cgs]
stability_database["cg_y"]=[cg[1] for cg in cgs]

# add +1 so that first waverider is waverider_2 (only do for first export)
stability_database.index=stability_database.index+1

# export updated database again
stability_database.to_excel(os.path.join('..','stability_database.xlsx'),index=True)