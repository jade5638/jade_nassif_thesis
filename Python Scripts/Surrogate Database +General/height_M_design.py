#%%
from setup import setup
import os
import numpy as np
from scipy.optimize import fsolve
import matplotlib.pyplot as plt
plt.rc('text', usetex=True)
plt.rc('font', family='serif')
from scipy.interpolate import interp1d
os.chdir("c:/Users/USER/OneDrive - Cranfield University/IRP/optimisation_new/")

vars=setup()

height=vars['height']
beta=vars['beta']
gamma=1.4

def cot(x):
    return 1/np.tan(x)

def theta_beta_m(beta, M_inf):
    global gamma

    beta = np.radians(beta)
    tan_theta=2 * cot(beta) * ((M_inf**2 * np.sin(beta)**2 - 1) / (M_inf**2 * (gamma + np.cos(2 * beta)) + 2))
    return tan_theta

def f(beta, theta, M_inf):
    global gamma

    beta = np.radians(beta)
    theta = np.radians(theta)
    return np.tan(theta) - 2 * cot(beta) * ((M_inf**2 * np.sin(beta)**2 - 1) / (M_inf**2 * (gamma + np.cos(2 * beta)) + 2))

def solve_for_beta(theta, M_inf):
    global gamma
    initial_guess = 20.0

    # Solve for beta using fsolve
    sol = fsolve(f, initial_guess, args=(theta, M_inf))
    
    return sol[0]

def calculate_height_M5(M_design):

    global beta
    deflection=np.arctan(theta_beta_m(beta=beta,M_inf=M_design))*180/np.pi
    new_beta_M5=solve_for_beta(theta=deflection,M_inf=5)
    new_height_M5=np.tan(np.radians(new_beta_M5))*7

    return new_height_M5
def calculate_height_M8(M_design):

    global beta
    deflection=np.arctan(theta_beta_m(beta=beta,M_inf=M_design))*180/np.pi
    new_beta_M8=solve_for_beta(theta=deflection,M_inf=8)
    new_height_M8=np.tan(np.radians(new_beta_M8))*7 

    return new_height_M8

def f1(M_design):
    global height
    h_M5=calculate_height_M5(M_design)
    h_M8=calculate_height_M8(M_design)

    abs_h_m5=np.abs(h_M5-height)
    abs_h_m8=np.abs(h_M8-height)

    return abs_h_m5-abs_h_m8



sol=fsolve(f1,6)
M_crit=sol[0]
n=1000

Mach=np.linspace(5,8,n)

heights_M5=np.zeros((n))
heights_M8=np.zeros((n))

for i,M in enumerate(Mach):

    heights_M5[i]=calculate_height_M5(M)
    heights_M8[i]=calculate_height_M8(M)



interp_height_M5=interp1d(Mach,heights_M5,kind='linear')
interp_height_M8=interp1d(Mach,heights_M8,kind='linear')

abs_heights_M5=np.abs(heights_M5-height)
abs_heights_M8=np.abs(heights_M8-height)

avg_deflection=np.mean((abs_heights_M8+abs_heights_M5)*.5)

M_plot=np.linspace(5,8,300)

def generate_height_fig():
    fig, ax = plt.subplots()


    ax.plot(M_plot, interp_height_M5(M_plot) - height, 'k-', label='Mach 5')
    ax.plot(M_plot, interp_height_M8(M_plot) - height, 'r-', label='Mach 8')
    ax.plot(M_plot, (interp_height_M8(M_plot) + interp_height_M5(M_plot)) / 2-height, '--b', label='Average')
    ax.plot([5, 8], [0, 0], 'm--', label='Design Height')

    ax.plot(M_crit,0, 'ok', label='$M_{crit}$', ms=7)
    # ax.plot((M_crit,M_crit),(0,interp_height_M8(5)-height), 'k--', ms=7)

    legend = ax.legend()
    legend.set_draggable(True)

    ax.set_xlabel(r'$M$\textsubscript{design}')
    ax.set_ylabel(r'$\Delta h$ [m]')
    ax.set_xlim([5, 8])
    ax.set_ylim([interp_height_M8(5)-height,interp_height_M5(8)-height])

    return fig

def generate_beta_fig():

    fig, ax = plt.subplots()


    ax.plot(M_plot, np.arctan(interp_height_M5(M_plot)/7)*180/np.pi, 'k-', label=r'$\beta_0$ at Mach 5')
    ax.plot(M_plot, np.arctan(interp_height_M8(M_plot)/7)*180/np.pi, 'r-', label=r'$\beta_0$ at Mach 8')
    ax.plot(M_plot, np.arctan((interp_height_M8(M_plot) + interp_height_M5(M_plot)) *0.5/7)*180/np.pi, '--b', label=r'Average $\beta_0$')
    ax.plot([5, 8], [beta, beta], 'm--', label='Design Shock Angle')

    ax.plot(M_crit,beta, 'ok', label=r'$M$\textsubscript{crit}', ms=7)
    # ax.plot((M_crit,M_crit),(0,interp_height_M8(5)-height), 'k--', ms=7)

    legend = ax.legend(fontsize=13)
    legend.set_draggable(True)

    ax.set_xlabel(r'$M$\textsubscript{design}',fontsize=13)
    ax.set_ylabel(r'$\beta_0$ [deg]',fontsize=13)
    ax.set_xlim([5, 8])
    # ax.set_ylim([interp_height_M8(5)-height,interp_height_M5(8)-height])

    return fig

fig1=generate_height_fig()
fig2=generate_beta_fig()
plt.show()
