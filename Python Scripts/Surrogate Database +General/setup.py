
def setup():
    # define waverider parameters
    height=1.876
    width=4.2
    beta=15
    constraint_value=((7/64)*(width/height)**4)*0.9  # multiply by 0.9 for computational errors

    # define the mach number range
    M_min=5
    M_max=8

    # define number of points desired
    n=100

    return {
        'height': height,
        'width': width,
        'beta': beta,
        'constraint_value': constraint_value,
        'M_min': M_min,
        'M_max': M_max,
        'n': n
    }

constraint_value=setup()['constraint_value']
def check_constraint(X1,X2):

    global constraint_value
    if X1!=1:
        if X2/((1-X1)**4)<constraint_value:
            return True
        else:
            return False
    else:
        return False
    
def is_dominated(solution_fitness, population_fitness):
    for fitness in population_fitness:
        if all(f >= s for f, s in zip(fitness, solution_fitness)) and any(f > s for f, s in zip(fitness, solution_fitness)):
            return True
    return False

gene_space = [
    {'low': 5, 'high': 8},
    {'low': 0, 'high': 1},  
    {'low': 0, 'high': 1},            
    {'low': 0, 'high': 1},             
    {'low': 0, 'high': 1}              
]