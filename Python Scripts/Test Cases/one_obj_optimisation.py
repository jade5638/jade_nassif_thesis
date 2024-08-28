#%%
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


with open("surrogate_models.pkl",'rb') as f:
    surrogate_models=pickle.load(f)
# with open("volume_rf.pkl",'rb') as f:
#     volume_rf=pickle.load(f)
volume_surrogate=surrogate_models['volume_surrogate']
L_M5_surrogate=surrogate_models['L_M5_surrogate']
L_M8_surrogate=surrogate_models['L_M8_surrogate']
D_M5_surrogate=surrogate_models['D_M5_surrogate']
D_M8_surrogate=surrogate_models['D_M8_surrogate']
s_wet_surrogate=surrogate_models['s_wet_surrogate']

vars=setup()

beta=vars['beta']
width=vars['width']
height=vars['height']
constraint_value=vars['constraint_value'] # already accounts for 0.9

base_lift_m5=65996
base_lift_m8=60866
base_drag_m5=9600
base_drag_m8=8951
def fitness_func(ga_instance,solution,solution_idx):
        
        # global volume_rf
        global volume_surrogate, s_wet_surrogate
        global L_M5_surrogate,L_M8_surrogate
        global D_M5_surrogate,D_M8_surrogate
        global base_lift_m5, base_lift_m8, base_drag_m5, base_drag_m8
        global check_constraint

        X1=solution[1]
        X2=solution[2]


        if check_constraint(X1,X2) :
            
            solution = np.array(solution).reshape(1, -1)

            L_M5=float(L_M5_surrogate.predict_values(solution))
            # L_M8=float(L_M8_surrogate.predict_values(solution))
            # D_M5=float(D_M5_surrogate.predict_values(solution))
            # D_M8=float(D_M8_surrogate.predict_values(solution))
            
            # volume_fitness=float(volume_rf.predict(solution))

            # volume_fitness=1/float(volume_surrogate.predict_values(solution))
            # s_wet_fitness=float(s_wet_surrogate.predict_values(solution))
            # v_eff_fitness=1/(volume_fitness/s_wet_fitness)
            lift_m5_fitness=1/(L_M5/base_lift_m5)
            # lift_m8_fitness=L_M8/base_lift_m8
            # drag_m5_fitness=(D_M5/base_drag_m5)
            # drag_m8_fitness=1/(D_M8/base_drag_m8)
            # delta_L_fitness=((L_M8-L_M5)/L_M5)*100
            # delta_D_fitness=-((D_M8-D_M5)/D_M5)*100

        else:
            # volume_fitness=0
            # v_eff_fitness=0
            lift_m5_fitness=0
            # drag_m5_fitness=0
        return lift_m5_fitness


# GA setup
num_generations = 1000
num_parents_mating = 40 
sol_per_pop = 70 
num_genes = 5

last_fitness = 0

def on_generation(ga_instance):

    global last_fitness

    print(f"Generation = {ga_instance.generations_completed}")
    # print(f"Fitness    = {ga_instance.best_solution(pop_fitness=ga_instance.last_generation_fitness)[1]}")
    # print(f"Change     = {ga_instance.best_solution(pop_fitness=ga_instance.last_generation_fitness)[1] - last_fitness}")
    last_fitness = ga_instance.best_solution(pop_fitness=ga_instance.last_generation_fitness)[1]

ga_instance = pygad.GA(num_generations=num_generations,
                        num_parents_mating=num_parents_mating,
                        sol_per_pop=sol_per_pop,
                        num_genes=num_genes,
                        fitness_func=fitness_func,
                        on_generation=on_generation,
                        gene_space=gene_space,
                        save_best_solutions=True,
                        crossover_type='uniform'
                        )

ga_instance.run()

ga_instance.plot_fitness(label=['v_eff'])
solution, solution_fitness, solution_idx = ga_instance.best_solution(ga_instance.last_generation_fitness)
print(f"Parameters of the best solution : {solution}")
print(f"Fitness value of the best solution = 1/{solution_fitness}")
print(f"Index of the best solution : {solution_idx}")
