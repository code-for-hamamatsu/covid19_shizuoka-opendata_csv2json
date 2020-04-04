import numpy as np

def is_nan(x):
    return (x is np.nan or x != x)
