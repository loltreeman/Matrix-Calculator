import numpy as np
from sympy import Matrix, pretty_print

def add_matrices(A, B):
    return np.add(A, B).tolist()

def subtract_matrices(A, B):
    return np.subtract(A, B).tolist()

def scalar_multiply(A, scalar):
    return np.multiply(A, scalar).tolist()

def gauss_elimination(A):
    A = np.array(A, dtype=float)
    rows, cols = A.shape
    for i in range(min(rows, cols)):
        if A[i, i] == 0:
            for j in range(i+1, rows):
                if A[j, i] != 0:
                    A[[i, j]] = A[[j, i]]
                    break
        if A[i, i] != 0:
            A[i] /= A[i, i]
        for j in range(i+1, rows):
            A[j] -= A[j, i] * A[i]
    return A.tolist()

def gauss_jordan_elimination(A):
    A = np.array(A, dtype=float)
    A = gauss_elimination(A)
    rows, cols = A.shape
    for i in range(rows-1, -1, -1):
        for j in range(i-1, -1, -1):
            A[j] -= A[j, i] * A[i]
    return A.tolist()
