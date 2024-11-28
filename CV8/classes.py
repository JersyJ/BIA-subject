import random
import numpy as np

class Config:
    def __init__(self, 
        num_cities: int,
        num_ants: int,
        num_iterations: int,
        alpha: float,
        beta: float,
        ep_rate: float,
        Q: float,
        distance_method       
    ):
        self.num_cities = num_cities
        self.num_ants = num_ants
        self.num_iterations = num_iterations
        self.alpha = alpha
        self.beta = beta
        self.ep_rate = ep_rate
        self.Q = Q
        self.distance_method = distance_method