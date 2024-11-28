from classes import Config
import numpy as np

def ant_colony_optimization(config: Config):

    def generatePheromones():
        return np.ones((config.num_cities, config.num_cities))

    def generateCities():
        return np.random.rand(config.num_cities, 2)

    # Initialization
    progress = []
    best_path_length = float('inf')
    pheromones = generatePheromones()
    cities = generateCities()
    
    # Iterate through iterations
    for _ in range(config.num_iterations):
        ants_paths, ants_paths_lengths = [], []
        
        # Iterate through ants
        for _ in range(config.num_ants):

            # Generate a matrix of visited points
            visited_cities = [False for _ in range(config.num_cities)]

            # Initialize ant - randomly visit any city and update path
            current_city = np.random.randint(config.num_cities)
            visited_cities[current_city] = True
            path = [current_city]
            path_length = 0
            
            # Visit all other cities
            while False in visited_cities:

                # List of all unvisited cities
                nonvisited_cities = np.where([not v for v in visited_cities])[0]

                # Initialize probabilities of visiting certain cities
                city_visit_probabilities = [0 for _ in range(len(nonvisited_cities))]
                
                # Iterate through all unvisited cities and generate probabilities of visiting them
                for i, unvisited_point in enumerate(nonvisited_cities):
                    left_side = np.power(pheromones[current_city, unvisited_point], config.alpha)
                    right_side = np.power(config.distance_method(cities[current_city], cities[unvisited_point]), config.beta)
                    city_visit_probabilities[i] =  left_side / right_side
                
                # Normalize all probabilities to be in range (0,1)
                city_visit_probabilities /= np.sum(city_visit_probabilities)
                
                # Choose next city to visit and update paths
                next_point = np.random.choice(nonvisited_cities, p=city_visit_probabilities)
                path_length += config.distance_method(cities[current_city], cities[next_point])
                visited_cities[next_point] = True
                current_city = next_point
                path.append(next_point)
            
            # Save path
            ants_paths.append(path)
            ants_paths_lengths.append(path_length)
            
            # Save best path
            if path_length < best_path_length:
                progress.append(path)
                best_path_length = path_length
        
        # For each path that all ants discovered update pheromones (influenced by variable Q)  
        pheromones *= config.ep_rate
        for path, path_length in zip(ants_paths, ants_paths_lengths):
            change = config.Q / path_length
            for i in range(config.num_cities-1):
                pheromones[path[i], path[i+1]] += change
            pheromones[path[-1], path[0]] += change
    
    return cities, progress