#%%
import numpy as np
from smt.sampling_methods import LHS

from sklearn.cluster import KMeans
import pandas as pd
random_state = np.random.RandomState(42)

from setup import setup
import os
os.chdir('C:\\Users\\USER\\OneDrive - Cranfield University\\IRP\\optimisation_new')
setup_variables=setup()

# define waverider parameters
height=setup_variables['height']
width=setup_variables['width']
beta=setup_variables['beta']
constraint_value=setup_variables['constraint_value']  # multiply by 0.9 for computational errors

# define the mach number range
M_min=setup_variables['M_min']
M_max=setup_variables['M_max']

# define number of points desired
n=setup_variables['n']

# define function which checks whether a point respects the constraint
def check_constraint(X1,X2):

    if X1==1:
        return False
    
    if X2/((1-X1)**4)<constraint_value:
        return True
    else:
        return False

# define the bounds
# in order: M, X1, X2, X3, X4, X5
bounds_X=np.array([0.0,1.0])
bounds=np.array([[M_min,M_max], bounds_X,bounds_X,bounds_X,bounds_X])

# initialise LHS instance
LHS_sampling=LHS(xlimits=bounds,random_state=random_state)

# intitialise initial sample
initial_sample=LHS_sampling(500)

# initialise valid samples array
valid_samples=np.empty((0,5))

for i,combination in enumerate(initial_sample):

    if check_constraint(combination[1],combination[2]):
        valid_samples=np.vstack((valid_samples,combination))

kmeans_clustering = KMeans(n_clusters=n, random_state=0, n_init="auto").fit(valid_samples)
final_sample_points=kmeans_clustering.cluster_centers_



columns = ['M_design', 'X1', 'X2', 'X3', 'X4']
df = pd.DataFrame(final_sample_points, columns=columns)
df.index=df.index+1

# export the first version of database. DO IT ONLY ONCE OTHERWISE ALL OTHER OUTPUTS WILL BE DELETED
# df.to_excel('database.xlsx', index=True)
# %%
