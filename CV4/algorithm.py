import random
from classes import Config
import time, math

# Calculating distance of all the cities whose order is randomized
def calculate_distance(cities: list, config: Config):
    sum = 0

    # Go through all cities in this combination
    for i in range(len(cities) - 1):
        city1 = cities[i]
        city2 = cities[i + 1]

        # Custom distance between them
        sum += config.distance_method(city1, city2)

    # In the end take first and last city distance
    city1 = cities[0]
    city2 = cities[-1]
    sum += config.distance_method(city1, city2)

    return sum

# Selecting the population - only once on start of algorithm 
def population_selection(config: Config): # cities, population_size

    # Contains total length of path and cities order
    population = []

    # Shuffle the list of cities and calculate its distance
    for i in range(config.population_size):
        c = config.cities.copy()
        random.shuffle(c)
        distance = calculate_distance(c, config)
        population.append([distance, c])

    # Take the one that has shortest length
    fitest = sorted(population)[0]

    # Return whole population with the fitest
    return population, fitest

# Main algorithm cycle
def algorithm_core(population: list, config: Config):
    iteration = 0
    cities_length = len(config.cities)
    sorted_population: list = sorted(population, key=lambda x: x[0])
    start_time = time.perf_counter()
    last_second: float = 0
    current_minimum: float = sorted_population[0][0]
    found_new_minimum = True
    best_population = []
    progress = []

    print(f"Start of the algorithm, generating {str(config.generations)} generations")
    print("-----------------------------------------------")
    print("Generations\tCurrent result\tChange")
    print("-----------------------------------------------")

    for _ in range(config.generations):

        # Initialization
        generation_time = time.perf_counter()
        run_time = generation_time - start_time
        second = math.floor(run_time)
        if (second != last_second and found_new_minimum == True) or (second - 10 >= last_second):
            last_second = second
            print(f"{str(iteration)}\t\t{str(round(sorted_population[0][0], 4))}   \t{'Shorter path found' if found_new_minimum == True else '-'}")
            found_new_minimum = False

        # Selecting two of the best options we have
        new_population = []
        new_population.append(sorted_population[0])
        new_population.append(sorted_population[1])

        # Go through half of the population
        for _ in range(int((len(population) - 2) / 2)):

            # Crossover (merging halves of two paths) - high chance
            if random.random() < config.crossover_rate:

                # Select random X points, sort them and select the first one (2x)
                parent_1 = sorted(random.choices(population, k=config.tournament_selection_size), key=lambda x: x[0])[0]
                parent_2 = sorted(random.choices(population, k=config.tournament_selection_size), key=lambda x: x[0])[0]

                # Get crossover line height
                point = random.randint(0, cities_length - 1)

                # Combine halves of parents paths and make sure they dont have same elements (cities)
                child_1 = parent_1[1][0:point]
                for city in parent_2[1]:
                    if (city in child_1) == False:
                        child_1.append(city)

                child_2 = parent_2[1][0:point]
                for city in parent_1[1]:
                    if (city in child_2) == False:
                        child_2.append(city)

            # If crossover doesn't happen, get two random paths and dont't change them - small chance
            else:
                child_1 = random.choices(population)[0][1]
                child_2 = random.choices(population)[0][1]

            # Mutation (change of cities between paths) - small chance
            if random.random() < config.mutation_rate:

                # Generate two random cities and change them between two paths
                city1 = random.randint(0, cities_length - 1)
                city2 = random.randint(0, cities_length - 1)
                child_1[city1], child_1[city2] = (
                    child_1[city2],
                    child_1[city1],
                )

                # Generate two random cities and change them between two paths
                city1 = random.randint(0, cities_length - 1)
                city2 = random.randint(0, cities_length - 1)
                child_2[city1], child_2[city2] = (
                    child_2[city2],
                    child_2[city1],
                )

            # Append two new paths into new population
            new_population.append([calculate_distance(child_1, config), child_1])
            new_population.append([calculate_distance(child_2, config), child_2])

        # Set new population as current
        population = new_population

        # Additional stuff
        sorted_population = sorted(population, key=lambda x: x[0])
        iteration += 1

        # If better was found - save it
        current = sorted_population[0][0]
        if current < current_minimum:
            current_minimum = current
            found_new_minimum = True
            best_population = sorted_population
            progress.append(best_population[1][1])

        # If target was found - end
        if sorted_population[0][0] < config.target:
            break

    answer = sorted(best_population, key=lambda x: x[0])[0]

    return answer, progress
