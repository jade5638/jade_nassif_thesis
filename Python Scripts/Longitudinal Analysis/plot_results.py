#%%
import os
import pandas as pd
import matplotlib.pyplot as plt
os.chdir(f"C:\\Users\\USER\\OneDrive - Cranfield University\\IRP\\optimisation_new\\Stability Analysis")

database=pd.read_excel('stability_database.xlsx',index_col=0,sheet_name='main')
plt.rc('text', usetex=True)
plt.rc('font', family='serif')
import numpy as np

def plot_angle_against_output(output: str, name: str, title: str, fontsize: int):
    global database

    fig, ax = plt.subplots(figsize=(5, 5))

    # generate a color map with 9 colors
    colors = plt.cm.brg(np.linspace(0, 1, 9))
    # marker styles to vary the markers
    markers = ['o', 's', '^']

    for i, idx in enumerate(database.index):
        pos_idx = database.index.get_loc(idx)
        color = colors[i % len(colors)]
        marker = markers[(i // 3) % len(markers)]
        
        alpha_neg_2_5 = database[f'{output}_alpha_neg_2_5'].iloc[pos_idx]
        alpha_0 = database[f'{output}_alpha_0'].iloc[pos_idx]
        alpha_pos_2_5 = database[f'{output}_alpha_pos_2_5'].iloc[pos_idx]
        ax.plot(
            [-2.5, 0, 2.5],
            [alpha_neg_2_5, alpha_0, alpha_pos_2_5],
            marker + '--', 
            color=color, 
            label=f'{database["Volume"].iloc[pos_idx]:.2f}'
        )
        
    ax.set_xlabel(r'$\alpha$ [deg]', fontsize=fontsize)
    ax.set_ylabel(name, fontsize=fontsize)
    ax.set_title(title, fontsize=fontsize)
    legend = ax.legend(title=r'Volume [m\textsuperscript{3}]', fontsize=fontsize,title_fontsize=fontsize)
    legend.set_draggable(True)
    
    return fig

fig=plot_angle_against_output(output='cp_x',name=r'$x$\textsubscript{CP}$/l$',title=r'$x$\textsubscript{CP}$/l$ against $\alpha$',fontsize=13)
plt.tight_layout()
fig=plot_angle_against_output(output='Lift',name=r'$L$ [N]',title=r'Lift against $\alpha$',fontsize=13)
plt.tight_layout()
fig=plot_angle_against_output(output='Drag',name=r'$D$ [N]',title=r'Drag against $\alpha$',fontsize=13)
plt.tight_layout()
fig=plot_angle_against_output(output='CM',name=r'$C$\textsubscript{M}',title=r'$C$\textsubscript{M} against $\alpha$',fontsize=13)
plt.tight_layout()

# calculate additional outputs in datavase
database['delta_LD_alpha_neg_2_5']=database['LD_alpha_0']-database['LD_alpha_neg_2_5']
database['delta_LD_alpha_pos_2_5']=database['LD_alpha_0']-database['LD_alpha_pos_2_5']
database['%_US_Lift_alpha_neg_2_5']=database['Lift_US_alpha_neg_2_5']/(database['Lift_alpha_neg_2_5']-database['Lift_US_alpha_neg_2_5'])
database['%_US_Lift_alpha_pos_2_5']=database['Lift_US_alpha_pos_2_5']/(database['Lift_alpha_pos_2_5']-database['Lift_US_alpha_pos_2_5'])

plt.show()

# database.to_excel('stability_database.xlsx',index=True)
