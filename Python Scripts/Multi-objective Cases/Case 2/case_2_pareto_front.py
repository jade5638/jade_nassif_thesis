#%%
import os
os.chdir(f"C:\\Users\\USER\\OneDrive - Cranfield University\\IRP\\optimisation_new")
import numpy as np
import pandas as pd
import sys
sys.path.append('')
from setup import is_dominated
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from scipy.spatial.distance import cdist
dir='Case 2'
os.chdir(f"C:\\Users\\USER\\OneDrive - Cranfield University\\IRP\\optimisation_new\\{dir}")
plt.rc('text', usetex=True)
plt.rc('font', family='serif')
# define fitness names and number of runs
fitness1='v_eff'
fitness2='drag_fitness'
n_runs=10
pareto_front=pd.DataFrame()

for i in range(1,n_runs+1):

    pf=pd.read_excel(f'{dir}.xlsx',sheet_name=f'Run {i}',index_col=0)

    pareto_front=pd.concat([pareto_front,pf],ignore_index=True)

pareto_front=pareto_front.sort_values(by=fitness1,ascending=True)

# get inverse again temporarily for non-dominated sorting
pareto_front[fitness2]=1/pareto_front[fitness2]

non_dominated_solutions = []

for i, current_solution in pareto_front.iterrows():
    if not is_dominated(np.array(current_solution[[fitness1,fitness2]]), np.array(pareto_front[[fitness1,fitness2]])):
        non_dominated_solutions.append(current_solution)

# create new df with only non-dominated solutions
pareto_front_filtered = pd.DataFrame(non_dominated_solutions)

# reobtain the inverse
pareto_front_filtered[fitness2]=1/pareto_front_filtered[fitness2]

plt.figure(figsize=(5,5))
plt.plot(pareto_front_filtered[fitness1],pareto_front_filtered[fitness2],'o',markersize=3,label='Pareto Solutions')
plt.xlabel(r'$v$\textsubscript{eff}',fontsize=13)
plt.ylabel('Drag Fitness',fontsize=13)
plt.title(f'Full Pareto Front for Case 2 ($n={len(pareto_front_filtered)}$) ',fontsize=13)
leg=plt.legend(fontsize=13)
leg.set_draggable(True)
plt.grid('on')
plt.tight_layout()

# set up Kmeans to cluster solutions
n_clusters=20
clustering=KMeans(n_clusters=n_clusters,random_state=30).fit(pareto_front_filtered[[fitness1,fitness2]])
centroids = clustering.cluster_centers_
representative_points = []
for i in range(n_clusters):

    cluster_points = pareto_front_filtered[clustering.labels_ == i]

    distances = cdist([centroids[i]], cluster_points[[fitness1,fitness2]])

    closest_index = np.argmin(distances)

    representative_point = cluster_points.iloc[closest_index]
    representative_points.append(representative_point)

representative_df = pd.DataFrame(representative_points)
representative_df=representative_df.sort_values(by=fitness1,ascending=True)

# check if the and min values are included in pareto front, if not add them and drop i=1 and i=len-2
max_index = pareto_front_filtered[fitness1].idxmax()
min_index = pareto_front_filtered[fitness1].idxmin()

if max_index not in representative_df.index:
    representative_df = pd.concat([representative_df, pareto_front_filtered.loc[[max_index]]])
    max_in=False
else:
    max_in=True


if min_index not in representative_df.index:
    representative_df = pd.concat([representative_df, pareto_front_filtered.loc[[min_index]]])
    min_in=False
else:
    min_in=True

# sort by fitness1 and reset index then drop the values of i=1 and i=len-1
representative_df = representative_df.sort_values(by=fitness1, ascending=True,ignore_index=True)

representative_df=representative_df.reset_index()
if min_in==False:
    representative_df=representative_df.drop([1])

if max_in==False:
    representative_df=representative_df.drop([len(representative_df)-1])
representative_df=representative_df.drop(columns=['index'])
representative_df=representative_df.reset_index()

# plot representative K-means pareto front
plt.figure(figsize=(5,5))
plt.plot(representative_df[fitness1], representative_df[fitness2], 'o--',label='Pareto Solutions')
plt.xlabel(r'$v$\textsubscript{eff}',fontsize=13)
plt.ylabel('Drag Fitness',fontsize=13)
plt.title(f'Pareto Front after K-means ($n={n_clusters}$) for Case 2',fontsize=13)
leg=plt.legend(fontsize=13)
leg.set_draggable(True)
plt.grid('on')
plt.tight_layout()

plt.show()