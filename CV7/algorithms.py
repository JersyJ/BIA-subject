import random
from classes import *
from copy import deepcopy

def soma_alltoone_yeah(config: SOMAConfiguration, population_size: int, iterations: int, prt: float, step: float, path_len: float):

    def generate_population(config: SOMAConfiguration, population_size: int) -> list:
        population = list()

        for _ in range(population_size):
            x: float = random.uniform(config.range_min, config.range_max)
            y: float = random.uniform(config.range_min, config.range_max)
            z: float = config.function(x, y)
            p = PointSOMA(x,y,z, generate_prt(prt))
            # p.clip_boundaries(config)
            population.append(p)

        return population    
    
    def generate_prt(prt):
        p_prt = Point(
            1 if np.random.uniform() < prt else 0,            
            1 if np.random.uniform() < prt else 0,
            0            
        )
        return p_prt
        # return [1 if np.random.uniform() < prt else 0 for _ in range(2)]
    
    def calc_position(point, leader, t) -> PointSOMA:
        new_position = (t * prt * (leader - point) + point)
        new_position.clip_boundaries(config)
        new_position.z = config.function(new_position.x, new_position.y)
        new_position.prt = Point(0,0,0)
        return new_position

    # 1. Generate population
    population = generate_population(config, population_size)

    # 2. Save original population into history
    history = []
    history.append(population)

    # 3. Iteration
    for _ in range(iterations):
        new_population = []

        # 3a. Find leader
        leader = min(population, key=lambda p: p.z)
        leader_index = population.index(leader)
        
        # 4. Population iteration
        for idx, p in enumerate(population):

            # 4a. Skip leader
            if idx == leader_index: continue
            p.prt = generate_prt(prt)
            t = 0
            jumps = list()

            # Perform jumps
            while t < path_len:
                new_point = calc_position(p, leader, t)
                jumps.append(new_point)
                t += step
            best_jump = min(jumps, key=lambda p: p.z)
            new_population.append(best_jump)
        
        population = deepcopy(new_population)
        population.append(leader)
        history.append(new_population)

    return history