import random
from classes import *
from copy import deepcopy

def particle_swarm_optimization(config: PSOConfiguration, population_size: int, iterations: int, w: float, c1: float, c2: float):
    # 1. Initialize particles (population) and velocities
    # 2. Evaluate best particles and positions
    # 3. Iterate X times
    #       a. Update velocities
    #       b. Update positions
    #       c. Evaluate fitness of particles
    #       d. Update best values

    def generate_population(config: PSOConfiguration, population_size: int) -> list:
        population = list()

        for i in range(population_size):
            x: float = random.uniform(config.range_min, config.range_max)
            y: float = random.uniform(config.range_min, config.range_max)
            z: float = config.function(x, y)
            p = PointPSO(x,y,z, Point(random.uniform(0, 1),random.uniform(0, 1),random.uniform(0, 1)))
            # p.clip_boundaries(config)
            population.append(p)

        return population    
    
    def update_velocity(config, particle: PointPSO, gbest: PointPSO, w, c1, c2) -> Point:
        r1 = random.uniform(0, 1)
        r2 = random.uniform(0, 1)
        velocity = w * particle.velocity + c1 * r1 * (particle.pbest - particle) + c2 * r2 * (gbest - particle)
        velocity.clip_velocity(config)
        return velocity

    # 1. Generate population (particles) with default velocity
    population = generate_population(config, population_size)

    # 2. Evaluate best point and pbest
    gbest_index = np.argmin([p.z for p in population])
    gbest = population[gbest_index]
    best_points = []
    progress = []

    # 3. Iterate
    for _ in range(iterations):
        progress.append(deepcopy(population))
        particle: PointPSO
        for idx, particle in enumerate(population):
            # a. Update velocity
            particle.velocity = update_velocity(config, particle, gbest, w, c1, c2)

            # b. c. Update position and evaluate fitness
            particle += particle.velocity
            particle.clip_boundaries(config)
            particle.z = config.function(particle.x, particle.y)

            # d. Update best values
            if particle.z < particle.pbest.z:
                particle.pbest = Point(particle.x, particle.y, particle.z)
                if particle.z < gbest.z:
                    gbest_index = idx
                    gbest = deepcopy(particle)
                    best_points.append(gbest)

        # d. Find best
        # gbest_index = np.argmin([p.z for p in population])
        # gbest = population[gbest_index]
        # best_points.append(gbest)
        # progress.append(population)
        print(gbest.z)

    return best_points, progress