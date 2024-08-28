#%%
import os
os.chdir("C:\\Users\\USER\\OneDrive - Cranfield University\\IRP\\optimisation_new")
from smt.surrogate_models import KRG
import pandas as pd
import matplotlib.pyplot as plt
plt.rc('text', usetex=True)
plt.rc('font', family='serif')
import numpy as np
from sklearn.model_selection import train_test_split
from smt.utils.misc import compute_rms_error
import warnings
# warnings.filterwarnings("ignore")
import pickle
from setup import setup

from smt.surrogate_models.krg import KRG
import numpy as np


'''
INITIALISATION
'''
setup_variables=setup()

# define the mach number range
M_min=setup_variables['M_min']
M_max=setup_variables['M_max']
constraint_value=setup_variables['constraint_value']
bounds_X=np.array([0.0,1.0])
bounds=np.array([[M_min,M_max], bounds_X,bounds_X,bounds_X,bounds_X])

# read all the data
database=pd.read_excel("database.xlsx",index_col=0)

# extract arrays
volume=np.array(database["Volume"]).reshape(-1,1)
s_wet=np.array(database['s_wet']).reshape(-1,1)
L_M5=np.array(database["Lift_M5"]).reshape(-1,1)
L_M8=np.array(database["Lift_M8"]).reshape(-1,1)
D_M5=np.array(database["Drag_M5"]).reshape(-1,1)
D_M8=np.array(database["Drag_M8"]).reshape(-1,1)
all_sample_points=np.array(database[["M_design","X1","X2","X3","X4"]])
#%%
'''
DATA SPLIT
'''
# split the data into training and test sets
# initial random state=30
test_size=0.1
random_state=30
points_train, points_test, volume_train, volume_test = train_test_split(all_sample_points, volume, test_size=test_size,random_state=random_state)
_, _, L_M5_train, L_M5_test = train_test_split(all_sample_points, L_M5, test_size=test_size,random_state=random_state)
_, _, L_M8_train, L_M8_test = train_test_split(all_sample_points, L_M8, test_size=test_size,random_state=random_state)
_, _, D_M5_train, D_M5_test = train_test_split(all_sample_points, D_M5, test_size=test_size,random_state=random_state)
_, _, D_M8_train, D_M8_test = train_test_split(all_sample_points, D_M8, test_size=test_size,random_state=random_state)
_, _, s_wet_train, s_wet_test = train_test_split(all_sample_points, s_wet, test_size=test_size,random_state=random_state)

# general function to evaluate performance of surrogate model. returns a figure, rms error for testing data, rms for training (should be 0) and the absolute error at every point in the testing
def evaluate_performance(surrogate_model: KRG,metric_test: np.ndarray, metric_train: np.ndarray,metric_name: str, units : str,fontsize: int):
    
    global points_test, points_train

    predicted_metric=surrogate_model.predict_values(points_test)
    RMS_error_test=compute_rms_error(sm=surrogate_model,xe=points_test,ye=metric_test)
    RMS_error_train=compute_rms_error(sm=surrogate_model,xe=points_train,ye=metric_train)
    abs_error=np.abs(((predicted_metric-metric_test)/metric_test)*100)

    fig, ax = plt.subplots()
    ax.plot(metric_test, predicted_metric, "ob",label='Testing Set')
    ax.plot([np.min(metric_test), np.max(metric_test)],
            [np.min(metric_test), np.max(metric_test)], 'r--')
    ax.set_xlabel(f"True " + metric_name +  " "+units,fontsize=fontsize)
    ax.set_ylabel("Predicted "+ metric_name + " "+ units,fontsize=fontsize)
    ax.set_title(f"\n RMS Error: {RMS_error_test:.5f}"+f'\n Max absolute error: {np.max(abs_error):.2f}\%',fontsize=fontsize)
    leg=ax.legend(fontsize=fontsize)
    leg.set_draggable(True)
    ax.grid(True)
    return fig,RMS_error_test,RMS_error_train,abs_error
#%%
'''
VOLUME
'''

volume_surrogate = KRG(print_training=False,
                       print_prediction=False,
                       print_problem=True,
                       print_solver=False,
                       poly='constant',
                       xlimits=bounds,
                       corr='squar_exp')

# train
volume_surrogate.set_training_values(points_train,volume_train)
volume_surrogate.train()
fig_volume,RMS_error_volume_test,RMS_error_volume_train,abs_error_volume=evaluate_performance(
                                                                surrogate_model=volume_surrogate,
                                                                metric_test=volume_test,
                                                                metric_train=volume_train,
                                                                metric_name='Volume',
                                                                units=r'[m\textsuperscript{3}]',
                                                                fontsize=13)
print(f'Test RMS Error (Volume): {RMS_error_volume_test}')
print(f'Train RMS Error (Volume): {RMS_error_volume_train}')
#%%
os.chdir("C:\\Users\\USER\\OneDrive - Cranfield University\\IRP\\Figures")
fig_volume.savefig('volume_surrogate_performance.pdf')
os.chdir("C:\\Users\\USER\\OneDrive - Cranfield University\\IRP\\optimisation_new")
#%%
'''
L_M5
'''
L_M5_surrogate = KRG(print_training=False,
                       print_prediction=False,
                       print_problem=True,
                       print_solver=False,
                       poly='constant',
                       xlimits=bounds)

# train
L_M5_surrogate.set_training_values(points_train,L_M5_train)
L_M5_surrogate.train()
fig_L_M5,RMS_error_L_M5_test,RMS_error_L_M5_train,abs_error_LM5=evaluate_performance(
                                                                surrogate_model=L_M5_surrogate,
                                                                metric_test=L_M5_test,
                                                                metric_train=L_M5_train,
                                                                metric_name=r'$L$\textsubscript{M5}',
                                                                units=r'[N]',
                                                                fontsize=13)
print(f'Test RMS Error (Lift @M5): {RMS_error_L_M5_test}')
print(f'Train RMS Error (Lift @M5): {RMS_error_L_M5_train}')
#%%
os.chdir("C:\\Users\\USER\\OneDrive - Cranfield University\\IRP\\Figures")
fig_L_M5.savefig('L_M5_surrogate_performance.pdf')
os.chdir("C:\\Users\\USER\\OneDrive - Cranfield University\\IRP\\optimisation_new")
#%%
'''
L_M8
'''
L_M8_surrogate = KRG(print_training=False,
                       print_prediction=False,
                       print_problem=True,
                       print_solver=False,
                       poly='constant',
                       xlimits=bounds)

# train
L_M8_surrogate.set_training_values(points_train,L_M8_train)
L_M8_surrogate.train()
fig_L_M8,RMS_error_L_M8_test,RMS_error_L_M8_train,abs_error_LM5=evaluate_performance(
                                                                surrogate_model=L_M8_surrogate,
                                                                metric_test=L_M8_test,
                                                                metric_train=L_M8_train,
                                                                metric_name=r'$L$\textsubscript{M8}',
                                                                units=r'[N]',
                                                                fontsize=13)
print(f'Test RMS Error (Lift @M8): {RMS_error_L_M8_test}')
print(f'Train RMS Error (Lift @M8): {RMS_error_L_M8_train}')
#%%
os.chdir("C:\\Users\\USER\\OneDrive - Cranfield University\\IRP\\Figures")
fig_L_M8.savefig('L_M8_surrogate_performance.pdf')
os.chdir("C:\\Users\\USER\\OneDrive - Cranfield University\\IRP\\optimisation_new")
#%%
'''
D_M5
'''
D_M5_surrogate = KRG(print_training=False,
                       print_prediction=False,
                       print_problem=True,
                       print_solver=False,
                       poly='constant',
                       xlimits=bounds)

# train
D_M5_surrogate.set_training_values(points_train,D_M5_train)
D_M5_surrogate.train()
fig_D_M5,RMS_error_D_M5_test,RMS_error_D_M5_train,abs_error_LM5=evaluate_performance(
                                                                surrogate_model=D_M5_surrogate,
                                                                metric_test=D_M5_test,
                                                                metric_train=D_M5_train,
                                                                metric_name=r'$D$\textsubscript{M5}',
                                                                units=r'[N]',
                                                                fontsize=13)
print(f'Test RMS Error (Drag @M5): {RMS_error_D_M5_test}')
print(f'Train RMS Error (Drag @M5): {RMS_error_D_M5_train}')
#%%
os.chdir("C:\\Users\\USER\\OneDrive - Cranfield University\\IRP\\Figures")
fig_D_M5.savefig('D_M5_surrogate_performance.pdf')
os.chdir("C:\\Users\\USER\\OneDrive - Cranfield University\\IRP\\optimisation_new")
#%%
'''
D_M8
'''
D_M8_surrogate = KRG(print_training=False,
                       print_prediction=False,
                       print_problem=True,
                       print_solver=False,
                       poly='constant',
                       xlimits=bounds)

# train
D_M8_surrogate.set_training_values(points_train,D_M8_train)
D_M8_surrogate.train()
fig_D_M8,RMS_error_D_M8_test,RMS_error_D_M8_train,abs_error_LM5=evaluate_performance(
                                                                surrogate_model=D_M8_surrogate,
                                                                metric_test=D_M8_test,
                                                                metric_train=D_M8_train,
                                                                metric_name=r'$D$\textsubscript{M8}',
                                                                units=r'[N]',
                                                                fontsize=13)
print(f'Test RMS Error (Drag @M8): {RMS_error_D_M8_test}')
print(f'Train RMS Error (Drag @M8): {RMS_error_D_M8_train}')
os.chdir("C:\\Users\\USER\\OneDrive - Cranfield University\\IRP\\Figures")
#%%
os.chdir("C:\\Users\\USER\\OneDrive - Cranfield University\\IRP\\Figures")
fig_D_M8.savefig('D_M8_surrogate_performance.pdf')
os.chdir("C:\\Users\\USER\\OneDrive - Cranfield University\\IRP\\optimisation_new")
# plt.show()
#%%
'''
s_wet
'''
s_wet_surrogate = KRG(print_training=False,
                       print_prediction=False,
                       print_problem=True,
                       print_solver=False,
                       poly='constant',
                       xlimits=bounds)

# train
s_wet_surrogate.set_training_values(points_train,s_wet_train)
s_wet_surrogate.train()
fig_s_wet,RMS_error_s_wet_test,RMS_error_s_wet_train,abs_error_LM5=evaluate_performance(
                                                                surrogate_model=s_wet_surrogate,
                                                                metric_test=s_wet_test,
                                                                metric_train=s_wet_train,
                                                                metric_name=r'$S$\textsubscript{wet}',
                                                                units=r'[m\textsuperscript{2}]',
                                                                fontsize=13)
print(f'Test RMS Error (s_wet): {RMS_error_s_wet_test}')
print(f'Train RMS Error (s_wet): {RMS_error_s_wet_train}')
#%%
os.chdir("C:\\Users\\USER\\OneDrive - Cranfield University\\IRP\\Figures")
fig_s_wet.savefig('s_wet_surrogate_performance.pdf')
os.chdir("C:\\Users\\USER\\OneDrive - Cranfield University\\IRP\\optimisation_new")
#%%
# serialise the surrogate models
with open("surrogate_models.pkl","wb") as f:
    pickle.dump({
        'volume_surrogate':volume_surrogate,
        'D_M5_surrogate':D_M5_surrogate,
        'D_M8_surrogate':D_M8_surrogate,
        'L_M5_surrogate':L_M5_surrogate,
        'L_M8_surrogate':L_M8_surrogate,
        's_wet_surrogate':s_wet_surrogate
    },f)