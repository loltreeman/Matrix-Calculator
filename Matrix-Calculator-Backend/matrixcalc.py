import numpy as np
from sympy import Matrix, pretty_print

def add_matrices(A, B):
    return np.add(A, B)

def subtract_matrices(A, B):
    return np.subtract(A, B)

def scalar_multiply(A, scalar):
    return np.multiply(A, scalar)

def interchange_rows(A, row1, row2):
    A[[row1, row2]] = A[[row2, row1]]
    return A

def multiply_row(A, row, scalar):
    A[row] *= scalar
    return A

def add_multiple_of_row(A, target_row, source_row, scalar):
    A[target_row] += scalar * A[source_row]
    return A

def gauss_elimination(A):
    A = A.astype(float)
    rows, cols = A.shape
    for i in range(min(rows, cols)):
        if A[i, i] == 0:
            for j in range(i+1, rows):
                if A[j, i] != 0:
                    interchange_rows(A, i, j)
                    break
        if A[i, i] != 0:
            multiply_row(A, i, 1 / A[i, i])
        for j in range(i+1, rows):
            if A[j, i] != 0:
                add_multiple_of_row(A, j, i, -A[j, i])
    return A

def gauss_jordan_elimination(A):
    A = gauss_elimination(A)
    rows, cols = A.shape
    for i in range(min(rows, cols)-1, -1, -1):
        for j in range(i-1, -1, -1):
            add_multiple_of_row(A, j, i, -A[j, i])
    return A

def solve_linear_system(A, b):
    augmented_matrix = np.hstack((A, b.reshape(-1, 1)))
    reduced_matrix = gauss_jordan_elimination(augmented_matrix)
    return reduced_matrix[:, -1]
