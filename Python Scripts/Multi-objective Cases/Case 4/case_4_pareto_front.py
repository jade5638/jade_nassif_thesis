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
dir='Case 4'
os.chdir(f"C:\\Users\\USER\\OneDrive - Cranfield University\\IRP\\optimisation_new\\{dir}")
plt.rc('text', usetex=True)
plt.rc('font', family='serif')
# define fitness names and number of runs
fitness1='Volume'
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
plt.xlabel(r'Volume [m\textsuperscript{3}]',fontsize=13)
plt.ylabel('Drag Fitness',fontsize=13)
plt.title(f'Full Pareto Front for Case 4 ($n={len(pareto_front_filtered)}$)',fontsize=13)
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
plt.plot(representative_df[fitness1], representative_df[fitness2], 'o--',markersize=5,label='Pareto Solutions')
plt.xlabel(r'Volume [m\textsuperscript{3}]',fontsize=13)
plt.ylabel('Drag Fitness',fontsize=13)
plt.title(f'Pareto Front after K-means ($n={n_clusters}$) for Case 4',fontsize=13)
leg=plt.legend(fontsize=13)
leg.set_draggable(True)
plt.grid('on')
plt.tight_layout()


# plt.show()
plt.figure(figsize=(5,5))
plt.plot(representative_df[fitness1], representative_df['M_design'], 'o--',markersize=5,label='Pareto Solutions')
plt.xlabel(r'Volume [m\textsuperscript{3}]',fontsize=13)
plt.ylabel(r'$M$\textsubscript{design}',fontsize=13)
plt.title(r'$M$\textsubscript{design} against Volume (Case 4 Pareto Front)',fontsize=13)
leg=plt.legend(fontsize=13)
leg.set_draggable(True)
plt.grid('on')
plt.tight_layout()
# plt.show()


X1_plot=[]
X1=np.array(representative_df['X1'])
X2=np.array(representative_df['X2'])
for x1,x2 in zip(X1,X2):
    if x2!=0:
        X1_plot.append(x1)
    else:
        X1_plot.append(0)

X1_plot=np.array(X1_plot)
# plot the variation of X1,X2 against Volume
plt.figure(figsize=(5,5))
plt.plot(representative_df[fitness1], X1_plot, 'x--k',markersize=5,label='X1')
plt.plot(representative_df[fitness1], representative_df['X2'], 'o--b',markersize=3,label='X2')
plt.axhline(y=0.2026, color='r', linestyle='--', xmin=0, xmax=1,label=r'X1\textsubscript{crit}')
plt.xlabel(r'Volume [m\textsuperscript{3}]',fontsize=13)
plt.ylabel('',fontsize=13)
plt.title('X1 and X2 against Volume (Case 4 Pareto Front)',fontsize=13)
leg=plt.legend(fontsize=13)
leg.set_draggable(True)
plt.grid('on')
plt.tight_layout()
# plt.show()


# plot variation of lift against drag/volume
plt.figure(figsize=(5,5))
plt.plot(representative_df[fitness1], representative_df['LD_M5'], 'o--',markersize=5,label='Pareto Solutions')
plt.xlabel(r'Volume [m\textsuperscript{3}]',fontsize=13)
plt.ylabel(r'$\left(L/D\right)$\textsubscript{M5}',fontsize=13)
plt.title(r'$\left(L/D\right)$\textsubscript{M5} against Volume (Case 4 Pareto Front)',fontsize=13)
leg=plt.legend(fontsize=13)
leg.set_draggable(True)
plt.grid('on')
plt.tight_layout()

# plt.show()


plt.figure(figsize=(5,5))
plt.plot(representative_df[fitness1], representative_df['v_eff'], 'o--',markersize=5,label='Pareto Solutions')
plt.xlabel(r'Volume [m\textsuperscript{3}]',fontsize=13)
plt.ylabel(r'$v$\textsubscript{eff}',fontsize=13)
plt.title(r'$v$\textsubscript{eff} against Volume (Case 4 Pareto Front)',fontsize=13)
leg=plt.legend(fontsize=13)
leg.set_draggable(True)
plt.grid('on')
plt.tight_layout()
plt.show()

'''
# check the accuracy of the surrogate model in predicting v_eff
from waverider_generator.generator import waverider as wr
from waverider_generator.cad_export import to_CAD
from setup import setup
vars=setup()
volumes=[]
s_wet=[]
for i,solution in representative_df.iterrows():

    waverider=wr(M_inf=solution['M_design'],
                    beta=vars['beta'],
                    height=vars['height'],
                    width=vars['width'],
                    dp=list(solution[['X1','X2','X3','X4']]),
                    n_upper_surface=10000,
                    n_shockwave=10000,
                    n_planes=30,
                    n_streamwise=30,
                    delta_streamwise=0.1)
    
    waverider_cad=to_CAD(waverider=waverider,sides='both',export=False,filename='na',scale=1000)
    faces=waverider_cad.val().Faces()
    volumes.append(waverider_cad.val().Volume()*1e-9)
    face_areas = [face.Area() for face in faces]
    #case where we have 6 faces so back is in two parts in CAD
    if len(face_areas)==6:

        smallest_face_area = 2*min(face_areas)
    # case where back is one face
    elif len(face_areas)==5:

        smallest_face_area = min(face_areas)
    s_wet.append((waverider_cad.val().Area() - smallest_face_area)*1e-6)

representative_df['true_volume']=volumes
representative_df['true_s_wet']=s_wet

plt.figure()
plt.plot(representative_df['true_volume'],representative_df['Volume'], 'o')
plt.plot([representative_df['true_volume'].min(),representative_df['true_volume'].max()],[representative_df['true_volume'].min(),representative_df['true_volume'].max()],'--')
# plt.show()

plt.figure()
plt.plot(representative_df['true_s_wet'],representative_df['s_wet'], 'o')
plt.plot([representative_df['true_s_wet'].min(),representative_df['true_s_wet'].max()],[representative_df['true_s_wet'].min(),representative_df['true_s_wet'].max()],'--')
plt.show()
RMS_vol=np.sqrt(np.mean((representative_df['true_volume'] - representative_df['Volume']) ** 2))
RMS_s_wet=np.sqrt(np.mean((representative_df['true_s_wet'] - representative_df['s_wet']) ** 2))
avg_abs_error_vol=np.mean(np.abs(representative_df['true_volume']-representative_df['Volume']))
avg_abs_error_s_wet=np.mean(np.abs(representative_df['true_s_wet']-representative_df['s_wet']))
'''