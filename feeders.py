import numpy as np

def random_sinoids():
    return np.sin(np.arange(100)*np.random.random(1)*5.0)

def random_positive_sinoids():
    return np.sin(np.arange(100)*np.random.random(1)*5.0) / 2.0 + 0.5
