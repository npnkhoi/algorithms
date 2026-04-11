import numpy as np

def matrix_from_file(path: str) -> np.ndarray:
    with open(path) as f:
        lines = f.readlines()
    matrix = np.array([
        line.split()
        for line in lines
    ]).astype(int)
    return matrix