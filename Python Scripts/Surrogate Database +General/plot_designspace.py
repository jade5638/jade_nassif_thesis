#%%
from setup import setup
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
os.chdir('C:\\Users\\USER\\OneDrive - Cranfield University\\IRP\\optimisation_new')

plt.rc('text', usetex=True)
plt.rc('font', family='serif')

setup_variables=setup()

# constraint and sample points
constraint_value=setup_variables['constraint_value'] 
database=pd.read_excel('database.xlsx',index_col=0)
final_sample_points=np.array(database[["M_design",'X1','X2','X3','X4']])

X1=np.linspace(0,1,1000)
X1_min=(constraint_value**0.25 - 1)/(constraint_value**0.25)
X2_min=constraint_value*(1-X1_min)**4
X2=[]
for i,x1 in enumerate(X1):
    if x1<=X1_min:
        X2.append(1)
    else:
        X2.append(constraint_value*(1-x1)**4)
X2=np.array(X2)
plt.figure()

plt.plot(X1, X2, label='Constraint Curve')
plt.plot(X1_min, X2_min, 'Dk', label=r'X1\textsubscript{crit} = '+f'{X1_min:.4f}')
plt.plot([0,X1_min],[X2_min,X2_min],'--k')
# ensure that only the first sample point gets the label 'Sample Point'
first_sample_point = True
for combination in final_sample_points:
    if first_sample_point:
        plt.plot(combination[1], combination[2], 'or', label='Sample Point')
        first_sample_point = False
    else:
        plt.plot(combination[1], combination[2], 'or')

plt.xlabel('X1',fontsize=13)
plt.ylabel('X2',fontsize=13)
plt.xlim((0,1))
plt.ylim((-0.05,1.1))
plt.title('Sampling across X1 and X2',fontsize=13)
leg=plt.legend(fontsize=13)
leg.set_draggable(True)
plt.grid(True)
plt.gca().set_aspect('equal', 'box')
plt.show()