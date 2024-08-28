#%%
import os
os.chdir("C:\\Users\\USER\\OneDrive - Cranfield University\\IRP\\optimisation_new")
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pickle
plt.rc('text', usetex=True)
plt.rc('font', family='serif')

database = pd.read_excel('database.xlsx',index_col=0)

# define the features
features= ['M_design', 'X1', 'X2', 'X3', 'X4']

def get_importances(output: str,output_name:str):
    fontsize=13
    global database, features

    X=database[features]
    y=database[[output]]

    rf = RandomForestRegressor(n_estimators=1000, random_state=30)

    rf.fit(X,y)

    train_accuracy=rf.score(X,y)

    print(f"Training Accuracy {output}: {train_accuracy}")
    
    feature_importances = rf.feature_importances_

    importance_df = pd.DataFrame({
    'Feature': [r'$M$\textsubscript{design}','X1','X2','X3','X4'],
    'Importance': feature_importances
    })
    importance_df = importance_df.sort_values(by='Importance', ascending=False)

    fig, ax = plt.subplots(figsize=(4, 4))
    sns.barplot(x='Importance', y='Feature', data=importance_df, ax=ax)
    ax.set_xlabel('Importance', fontsize=fontsize)
    ax.tick_params(axis='x', labelsize=fontsize)
    ax.tick_params(axis='y', labelsize=fontsize)
    ax.set_ylabel('')
    ax.set_title('Feature Importance for '+ output_name,fontsize=fontsize)
    return fig,rf,X,y

Volume=get_importances('Volume','Volume')
plt.tight_layout(pad=1.0)
drag_m5=get_importances('Drag_M5',r'$D$\textsubscript{M5}')
plt.tight_layout(pad=1.0)
lift_m5=get_importances('Lift_M5',r'$L$\textsubscript{M5}')
plt.tight_layout(pad=1.0)
LD_M5=get_importances('LD_M5',r'$\left(L/D\right)$\textsubscript{M5}')
plt.tight_layout(pad=1.0)

plt.show()