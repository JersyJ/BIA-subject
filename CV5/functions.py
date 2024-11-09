import numpy as np

def sphere(x: float, y: float):
    return x**2.0 + y**2.0

def griewank(x: float, y: float):
    return ((x**2 + y**2) / 4000) - (np.cos(x / np.sqrt(2)) * np.cos(y / np.sqrt(2))) + 1

def rosenbrock(x: float, y: float):
    return (1 - x) ** 2 + 100.0 * (y - x**2) ** 2

def schwefel(x: float, y: float):
    return 418.9829 * 2 - x * np.sin(np.sqrt(abs(x))) - y * np.sin(np.sqrt(abs(y)))

def rastrigin(x: float, y: float):
    return (x**2 + y**2 - 10 * (np.cos(2 * np.pi * x) + np.cos(2 * np.pi * y))) + 20

def ackley(x: float, y: float):
    return (
        -20.0 * np.exp(-0.2 * np.sqrt(0.5 * (x**2 + y**2)))
        - np.exp(0.5 * (np.cos(2 * np.pi * x) + np.cos(2 * np.pi * y)))
        + np.e
        + 20
    )

def michalewicz(x: float, y: float):
    return -1 * ( (np.sin(x) * np.sin((1 * x**2) / np.pi) ** 20) + (np.sin(y) * np.sin((2 * y**2) / np.pi) ** 20) )

def zakharov(x: float, y: float):
    return x**2 + y**2 + pow(0.5 * x + y, 2) + pow(0.5 * x + y, 4)

def levy(x: float, y: float):
    a = (
        np.sin(3 * np.pi * x) ** 2
        + (x - 1) ** 2 * (1 + np.sin(3 * np.pi * y) * np.sin(3 * np.pi * y))
        + (y - 1) * (y - 1) * (1 + np.sin(2 * np.pi * y) * np.sin(2 * np.pi * y))
    )
    return a
