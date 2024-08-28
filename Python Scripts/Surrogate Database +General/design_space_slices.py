
#%%
import os
os.chdir("C:\\Users\\USER\\OneDrive - Cranfield University\\IRP\\optimisation_new")
import pandas as pd
import matplotlib.pyplot as plt

plt.rc('text', usetex=True)
plt.rc('font', family='serif')

database = pd.read_excel('database.xlsx',index_col=0)
#%%
def plot_outputs(output1: str,output2: str,name1 : str, name2: str, grid: bool, title:str, fontsize: int,**kwargs):

    output1_data=database[[output1]]
    output2_data=database[[output2]]

    fig, ax = plt.subplots(figsize=(5,5))
    ax.scatter(output1_data,output2_data,color='r',label='Sample Point',s=15)
    ax.set_xlabel(name1,fontsize=fontsize)
    ax.set_ylabel(name2,fontsize=fontsize)
    ax.set_title(title,fontsize=fontsize)

    ax.grid(grid)
    if 'xlim' in kwargs:

        ax.set_xlim(kwargs['xlim'])
    if 'ylim' in kwargs:  
        ax.set_ylim(kwargs['ylim'])
    if 'aspect_ratio' in kwargs:
        if kwargs['aspect_ratio']==True:
            ax.set_aspect('equal', 'box')

    if 'plot_x_equal_y' in kwargs:
        if kwargs['plot_x_equal_y']==True:
            xlim=ax.get_xlim()
            xmin=xlim[0]
            xmax=xlim[1]
           
            ax.plot([xmin ,xmax],[xmin,xmax],'--k',label="x=y line")
            ax.set_xlim(xlim)
    leg=ax.legend(fontsize=fontsize)
    leg.set_draggable(True)
    return fig

fig=plot_outputs(output1='X3',output2='X4',name1='X3',name2='X4',grid=True,title='Sampling across X3 and X4',fontsize=13,xlim=(0,1),ylim=(0,1),aspect_ratio=True)
plt.tight_layout()
fig=plot_outputs(output1='Lift_M5',output2='Lift_M8',name1=r'$L$\textsubscript{M5} [N]',name2=r'$L$\textsubscript{M8} [N]',grid=True,title=r'$L$\textsubscript{M8} against $L$\textsubscript{M5}',fontsize=13,aspect_ratio=False,plot_x_equal_y=True)
plt.tight_layout()
fig=plot_outputs(output1='LD_M5',output2='LD_M8',name1=r'$\left(L/D\right)$\textsubscript{M5}',name2=r'$\left(L/D\right)$\textsubscript{M8}',grid=True,title=r'$\left(L/D\right)$\textsubscript{M8} against $\left(L/D\right)$\textsubscript{M5}',fontsize=13,aspect_ratio=False,plot_x_equal_y=True)
plt.tight_layout()
fig=plot_outputs(output1='Drag_M5',output2='Drag_M8',name1=r'$D$\textsubscript{M5} [N]',name2=r'$D$\textsubscript{M8} [N]',grid=True,title=r'$D$\textsubscript{M8} against $D$\textsubscript{M5}',fontsize=13,aspect_ratio=False,plot_x_equal_y=True)
plt.tight_layout()
fig=plot_outputs(output1='Volume',output2='Drag_M5',name1=r'Volume [m\textsuperscript{3}]',name2=r'$D$\textsubscript{M5} [N]',grid=True,title=r'$D$\textsubscript{M5} against Volume',fontsize=13,aspect_ratio=False,plot_x_equal_y=False)
plt.tight_layout()
fig=plot_outputs(output1='Volume',output2='LD_M5',name1=r'Volume [m\textsuperscript{3}]',name2=r'$\left(L/D\right)$\textsubscript{M5}',grid=True,title=r'',fontsize=13,aspect_ratio=False,plot_x_equal_y=False)
plt.tight_layout()
fig=plot_outputs(output1='Volume',output2='Lift_M5',name1=r'Volume [m\textsuperscript{3}]',name2=r'$L$\textsubscript{M5} [N]',grid=True,title=r'$L$\textsubscript{M5} against Volume',fontsize=13,aspect_ratio=False,plot_x_equal_y=False)
plt.tight_layout()
fig=plot_outputs(output1='Volume',output2='v_eff',name1=r'Volume [m\textsuperscript{3}]',name2=r'$v$\textsubscript{eff}',grid=True,title=r'$v$\textsubscript{eff} against Volume',fontsize=13,aspect_ratio=False,plot_x_equal_y=False)
plt.tight_layout()
fig=plot_outputs(output1='Volume',output2='Drag_visc_M5',name1=r'Volume [m\textsuperscript{3}]',name2=r'$D$\textsubscript{M5} [N]',grid=True,title=r'$D$\textsuperscript{visc}\textsubscript{M5} against Volume',fontsize=13,aspect_ratio=False,plot_x_equal_y=False)
plt.tight_layout()
fig=plot_outputs(output1='M_design',output2='Drag_M5',name1=r'$M$\textsubscript{design}',name2=r'$D$\textsubscript{M5} [N]',grid=True,title=r'$D$\textsubscript{M5} against $M$\textsubscript{design}',fontsize=13,xlim=(5,8),aspect_ratio=False)
plt.tight_layout()
fig=plot_outputs(output1='M_design',output2='Lift_M5',name1=r'$M$\textsubscript{design}',name2=r'$L$\textsubscript{M5} [N]',title=r'$L$\textsubscript{M5} against $M$\textsubscript{design}',fontsize=13,xlim=(5,8),aspect_ratio=False,grid=True)
plt.tight_layout()
fig=plot_outputs(output1='M_design',output2='LD_M5',name1=r'$M$\textsubscript{design}',name2=r'$\left(L/D\right)$\textsubscript{M5}',grid=True,title=r'$\left(L/D\right)$\textsubscript{M5} against $M$\textsubscript{design}',fontsize=13,xlim=(5,8),aspect_ratio=False)
plt.tight_layout()
fig=plot_outputs(output1='X2',output2='Volume',name1=r'X2',name2=r'Volume [m\textsuperscript{3}]',grid=True,title=r'Volume against X2',fontsize=13,aspect_ratio=False)
plt.tight_layout()
fig=plot_outputs(output1='M_design',output2='Volume',name1=r'$M$\textsubscript{design}',name2=r'Volume',grid=True,title=r'Volume against $M$\textsubscript{design}',fontsize=13,xlim=(5,8),aspect_ratio=False)
plt.tight_layout()
fig=plot_outputs(output1='v_eff',output2='Drag_M5',name1=r'$v$\textsubscript{eff}',name2=r'$D$\textsubscript{M5} [N]',grid=True,title=r'$D$\textsubscript{M5} against $v$\textsubscript{eff}',fontsize=13,aspect_ratio=False)
plt.tight_layout()
plt.show()
