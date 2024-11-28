import random

class City:
    def __init__(self, 
        id: int,
        x: float,
        y: float     
    ):
        self.id = id
        self.x = x
        self.y = y

class Config:
    def __init__(self, 
        population_size: int,
        tournament_selection_size: int,
        mutation_rate: float,
        generations: int,
        crossover_rate: float,
        cities_file,
        cities_length: int,
        distance_method,
        target: float = 0,       
    ):
        self.population_size = population_size
        self.tournament_selection_size = tournament_selection_size
        self.mutation_rate = mutation_rate
        self.generations = generations
        self.crossover_rate = crossover_rate
        self.target = target
        self.distance_method = distance_method
        self.cities = list()
        if cities_file is not None:
            self.cities_file = cities_file
            self.loadCities()
        else:
            self.cities_file = "generated"
            self.generateCities(cities_length)

    def generateCities(self, length):
        for i in range(0, length):
            randomX = random.randint(0, 100)
            randomY = random.randint(0, 100)
            self.cities.append(
                City(
                    id=i,
                    x=randomX,
                    y=randomY
                )
            )

    def loadCities(self):
        with open(self.cities_file) as f: 
            for line in f.readlines():
                city_info = line.split()
                self.cities.append(
                    City(id=city_info[0], 
                        x=float(city_info[1]), 
                        y=float(city_info[2])
                    )
                )