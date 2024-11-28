import math
import numpy as np

def euclidean_numpy(point1, point2):
    return np.sqrt(np.sum((point1 - point2)**2))