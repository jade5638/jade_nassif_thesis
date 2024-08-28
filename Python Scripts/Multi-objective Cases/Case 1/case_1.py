#%%
'''
OPTIMISATION FOR CASE 1
'''
import os
os.chdir("C:\\Users\\USER\\OneDrive - Cranfield University\\IRP\\optimisation_new")
import pickle
import pygad
import numpy as np
import warnings
from waverider_generator.generator import waverider as wr
from waverider_generator.cad_export import to_CAD
warnings.filterwarnings("ignore")
from matplotlib import pyplot as plt
from setup import setup, check_constraint, is_dominated, gene_space
import pandas as pd
plt.rc('text', usetex=True)
plt.rc('font', family='serif')

# import surrogate models
with open("surrogate_models.pkl",'rb') as f:
    surrogate_models=pickle.load(f)


volume_surrogate=surrogate_models['volume_surrogate']
L_M5_surrogate=surrogate_models['L_M5_surrogate']
L_M8_surrogate=surrogate_models['L_M8_surrogate']
D_M5_surrogate=surrogate_models['D_M5_surrogate']
D_M8_surrogate=surrogate_models['D_M8_surrogate']
s_wet_surrogate=surrogate_models['s_wet_surrogate']

vars=setup()

# get parameters for post processing
beta=vars['beta']
width=vars['width']
height=vars['height']
constraint_value=vars['constraint_value'] # already accounts for 0.9

# quantities given in Table 10
base_lift_m5=65996
base_lift_m8=60866
base_drag_m5=9600
base_drag_m8=8951

def fitness_func(ga_instance,solution,solution_idx):

        global volume_surrogate
        global D_M5_surrogate,D_M8_surrogate
        global base_drag_m5, base_drag_m8
        global check_constraint

        X1=solution[1]
        X2=solution[2]


        if check_constraint(X1,X2) :
            
            #reshape to enter into surrogate models
            solution = np.array(solution).reshape(1, -1)

            # get volume
            volume_fitness=float(volume_surrogate.predict_values(solution))

            # get drag
            D_M5=float(D_M5_surrogate.predict_values(solution))
            D_M8=float(D_M8_surrogate.predict_values(solution))
            D_avg=((D_M8*0.5+D_M5*0.5)/(0.5*base_drag_m5+0.5*base_drag_m8))
            drag_fitness=1/D_avg

        else:
            volume_fitness=0
            drag_fitness=0
        return volume_fitness,drag_fitness


# GA setup
num_generations = 2500
num_parents_mating = 70 
sol_per_pop = 100 
num_genes = 5

last_fitness = 0

def on_generation(ga_instance):

    global last_fitness

    print(f"Generation = {ga_instance.generations_completed}")
    # print(f"Fitness    = {ga_instance.best_solution(pop_fitness=ga_instance.last_generation_fitness)[1]}")
    # print(f"Change     = {ga_instance.best_solution(pop_fitness=ga_instance.last_generation_fitness)[1] - last_fitness}")
    last_fitness = ga_instance.best_solution(pop_fitness=ga_instance.last_generation_fitness)[1]

# initialise the GA instance
ga_instance = pygad.GA(num_generations=num_generations,
                        num_parents_mating=num_parents_mating,
                        sol_per_pop=sol_per_pop,
                        num_genes=num_genes,
                        fitness_func=fitness_func,
                        on_generation=on_generation,
                        parent_selection_type='nsga2',
                        gene_space=gene_space,
                        save_best_solutions=True,
                        crossover_type='uniform')

# run
ga_instance.run()

from plyer import notification
notification.notify(
    title='CASE 1',
    message='Optimisation Done',
    app_name='VS Code',
    timeout=10  # seconds
)

fitness1='Volume'
fitness2='drag_fitness'

# ga_instance.plot_fitness(label=[fitness1,fitness2])

# extract last population and corresponding fitness
last_population = ga_instance.population
last_population_fitness = ga_instance.last_generation_fitness

pareto_solutions = []

pareto_fitness = []

# get pareto (non dominated solutions)
for sol, fit in zip(last_population, last_population_fitness):
    if not is_dominated(fit, last_population_fitness):
        pareto_solutions.append(sol)
        pareto_fitness.append(fit)


pareto_solutions = np.array(pareto_solutions)
pareto_fitness = np.array(pareto_fitness)

pareto=np.concatenate((pareto_solutions,pareto_fitness),axis=1)
column_names = ['M_design', 'X1', 'X2', 'X3', 'X4', fitness1, fitness2]

pareto_df=pd.DataFrame(pareto, columns=column_names)

pareto_df[fitness2]=1/pareto_df[fitness2]

L_M5=[]
L_M8=[]
D_M5=[]
D_M8=[]
s_wet=[]

# get other quantities from design space
for solution in pareto_solutions:
    solution = np.array(solution).reshape(1, -1)
    L_M5.append(float(L_M5_surrogate.predict_values(solution)))
    L_M8.append(float(L_M8_surrogate.predict_values(solution)))
    D_M5.append(float(D_M5_surrogate.predict_values(solution)))
    D_M8.append(float(D_M8_surrogate.predict_values(solution)))
    s_wet.append(float(s_wet_surrogate.predict_values(solution)))

pareto_df['s_wet']=s_wet
pareto_df['v_eff']=pareto_df[fitness1]**(2/3)/pareto_df['s_wet']
pareto_df['L_M5'] = L_M5
pareto_df['L_M8'] = L_M8
pareto_df['D_M5'] = D_M5
pareto_df['D_M8'] = D_M8
pareto_df['LD_M5']=pareto_df['L_M5']/pareto_df['D_M5']
pareto_df['LD_M8']=pareto_df['L_M8']/pareto_df['D_M8']

# sort solutions based on volume
pareto_df = pareto_df.sort_values(by=fitness1, ascending=True)

plt.figure()
plt.plot(pareto_df[fitness1],pareto_df[fitness2],'o--')
plt.xlabel(fitness1)
plt.ylabel(fitness2)

plt.show()

#%%
import os
i=10

# checklist
'''
i=1 --> done
i=2 --> done
i=3 --> done
i=4 --> done
i=5 --> done
i=6 --> done
i=7 --> done
i=8 --> done
i=9 --> done
i=10 --> done
'''
dir='Case 1'

os.chdir(f"C:\\Users\\USER\\OneDrive - Cranfield University\\IRP\\optimisation_new\\{dir}")

with pd.ExcelWriter(f'{dir}.xlsx', engine='openpyxl', mode='a', if_sheet_exists='new') as writer:
    pareto_df.to_excel(writer, sheet_name=f'Run {i}', index=True)
