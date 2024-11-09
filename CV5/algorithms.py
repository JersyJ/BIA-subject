import random
from classes import *
import numpy

# Differential evolution
def differential_evolution(config : DEConfiguration, population_size: int, iterations: int, mutation_rate: float, crossover_rate: float):
    
    # 1. Generate population - random points
    # 2. Loop iterations (generations)
    #       a. Loop population
    #           1. Select three random points
    #           2. Create mutation point and check bounds (create new point from X and Y coords 
    #              from three random points selected earlier and also check if point is not out of bounds)
    #           3. Create empty (target) point - new empty point
    #           4. Loop through every dimension of point (go through X and Y coords
    #              and either take them from original point or from mutation point)
    #               a. Either randomly save parameter from mutation (save coord from mutation)
    #               b. Or save parameter from original point (save coord from original point)
    #           5. Evaluate new generated point (get Z coord)
    #           6. If better or same - replace it in population
    #       b. Get the best point and print it (save it)

    def generate_population(config: DEConfiguration, population_size: int) -> list:
        population = list()

        for i in range(population_size):
            x: float = random.uniform(config.range_min, config.range_max)
            y: float = random.uniform(config.range_min, config.range_max)
            z: float = config.function(x, y)
            population.append(Point(x,y,z))

        return population    

    # 1. Generate population
    population = generate_population(config, population_size)
    for p in population:
        print(p.z)
    best_point = population[0]
    start_point = best_point
    all_points = list()

    # 2. Loop iterations (generations)
    for _ in range(iterations):
        
        # a. Loop population (points)
        for idx, point in enumerate(population):

            # 1. Select three random points
            candidates = [candidate for candidate in range(population_size) if candidate != idx]
            chosen_candidates = numpy.random.choice(candidates, 3, replace=False)
            p1 = population[chosen_candidates[0]]
            p2 = population[chosen_candidates[1]]
            p3 = population[chosen_candidates[2]]

            # 2. Create mutation vector and check bounds
            mutation_vector = (p1 - p2) * mutation_rate + p3
            mutation_vector.clip_boundaries(config)

            # 3. Create empty (target) vector
            target_vector = Point(0, 0, 0)

            # 4. Loop through every dimension of point - crossover
            dimensions = 2
            random_dimension = numpy.random.randint(0, dimensions)
            for dimension in range(dimensions):

                # a. Either randomly save parameter from mutation
                if numpy.random.uniform() < crossover_rate or dimension == random_dimension:
                    target_vector[dimension] = mutation_vector[dimension]
                
                # b. Or save parameter from original point
                else:
                    target_vector[dimension] = point[dimension]
            
            # 5. Evaluate new generated point
            target_vector.z = config.function(target_vector.x, target_vector.y)

            # 6. If better or same - replace it in population
            if target_vector.z <= point.z:
                population[idx] = target_vector
        
        # b. Get the best point and print it (save it)
        for p in population:
            if p.z < best_point.z:
                best_point = p
        
        all_points.append(best_point)
        # print(f"[ALGO] Current best z: {best_point.z}")

    print(f"[ALGO] Best result after {iterations} generations and population size {population_size}: {best_point.z}")
    return best_point, all_points, start_point
