from classes import City
import math
import numpy as np

def euclidean(city1: City, city2: City) -> float:
    return math.sqrt(math.pow(city2.x - city1.x, 2) + math.pow(city2.y - city1.y, 2))

def manhattan(city1, city2):
    return (np.abs(city1.x - city1.y) + np.abs(city2.x - city2.y))