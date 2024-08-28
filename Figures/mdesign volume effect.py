#%%
from waverider_generator.generator import waverider as wr
from waverider_generator.cad_export import to_CAD
import matplotlib.pyplot as plt
plt.rc('text', usetex=True)
plt.rc('font', family='serif')
import numpy as np
height=1.876
width=4.2
beta=15
mdesigns=[5,6.5,8]
waveriders=[]
waveriders_cad=[]
for m in mdesigns:
    waverider=wr(M_inf=m,
                 beta=beta,
                 height=height,
                 width=width,
                 dp=[0.1,0.5,0.5,1],
                 n_upper_surface=10000,
                 n_shockwave=10000,
                 n_planes=60,
                 n_streamwise=30,
                 delta_streamwise=0.1)
    waveriders.append(waverider)
    
    to_CAD(waverider=waverider,sides='both',export=False,filename='prout',scale=1000)
#%%    
fontsize=13
plt.figure()
waverider=waveriders[0]
inters=waverider.local_intersections_us
inters=np.vstack([np.array([0,waverider.height]),inters,waverider.us_P3])
plt.plot(inters[:, 0], inters[:, 1], 'k-',label="USC")
shockwave=np.column_stack([waverider.z_local_shockwave,waverider.y_local_shockwave])
shockwave=np.vstack([np.array([0,0]),shockwave,waverider.s_P4])
plt.plot(shockwave[:, 0], shockwave[:, 1], '--',color='black',label="SC")
for waverider,mdesign in zip(waveriders,mdesigns):
    lower_surface=waverider.lower_surface_streams
    lower_surface = np.vstack([stream[-1,:] for stream in lower_surface])
    z_ls=lower_surface[:,2]
    y_ls = lower_surface[:,1]+waverider.height
    plt.plot(z_ls, y_ls, '-',label=r"LSC for $M$\textsubscript{design}"+f"$={mdesign}$")
plt.xlabel('$z$ [m]',fontsize=fontsize)
plt.ylabel(r'$\overline{y}$ [m]',fontsize=fontsize)
plt.gca().set_aspect('equal') 
leg=plt.legend(fontsize=fontsize)
leg.set_draggable(True)
plt.xlim((0,waverider.width))
plt.title(r'[X1,X2,X3,X4]='+f'[{waverider.X1:.2f},{waverider.X2:.2f},{waverider.X3:.2f},{waverider.X4:.2f}]',fontsize=fontsize)
plt.gca().spines['right'].set_visible(False)  # Hides the right spine
plt.gca().spines['top'].set_visible(False)
plt.tight_layout()
plt.show()