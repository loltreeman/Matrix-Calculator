import json
import numpy as np
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt  # Disable CSRF for now (use Django REST Framework for production)
def calculate_matrix(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            matrixA = parse_matrix(data.get("matrixA"))
            matrixB = parse_matrix(data.get("matrixB")) if data.get("matrixB") else None
            operation = data.get("operation")

            if matrixA is None or (operation in ["add", "subtract"] and matrixB is None):
                return JsonResponse({"error": "Invalid matrix input"}, status=400)

            # Perform the requested operation
            if operation == "add":
                result = np.add(matrixA, matrixB).tolist()
            elif operation == "subtract":
                result = np.subtract(matrixA, matrixB).tolist()
            elif operation == "scalar":
                scalar = float(data.get("scalar", 1))  # Default scalar is 1
                result = (np.array(matrixA) * scalar).tolist()
            elif operation == "gauss":
                result = gaussian_elimination(matrixA)
            elif operation == "jordan":
                result = gauss_jordan_elimination(matrixA)
            else:
                return JsonResponse({"error": "Invalid operation"}, status=400)

            return JsonResponse({"result": result}, status=200)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Invalid request"}, status=400)


def parse_matrix(matrix_str):
    """ Convert a string like '2,1,-1;1,3,2;1,-1,2' into a list of lists """
    try:
        return [list(map(float, row.split(","))) for row in matrix_str.split(";")]
    except ValueError:
        return None


def gaussian_elimination(matrix):
    """ Perform Gaussian elimination (convert to row echelon form) """
    A = np.array(matrix, dtype=float)
    rows, cols = A.shape

    for i in range(min(rows, cols)):
        max_row = np.argmax(np.abs(A[i:, i])) + i
        A[[i, max_row]] = A[[max_row, i]]

        if A[i, i] == 0:
            continue

        A[i] /= A[i, i]
        for j in range(i + 1, rows):
            A[j] -= A[i] * A[j, i]

    return A.tolist()


def gauss_jordan_elimination(matrix):
    """ Perform Gauss-Jordan elimination (convert to reduced row echelon form) """
    A = np.array(matrix, dtype=float)
    rows, cols = A.shape

    for i in range(min(rows, cols)):
        max_row = np.argmax(np.abs(A[i:, i])) + i
        A[[i, max_row]] = A[[max_row, i]]

        if A[i, i] == 0:
            continue

        A[i] /= A[i, i]
        for j in range(rows):
            if j != i:
                A[j] -= A[i] * A[j, i]

    return A.tolist()
