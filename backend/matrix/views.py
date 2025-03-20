import json
import numpy as np  
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt  # Disable CSRF for now (for production consider using Django REST Framework)
def calculate_matrix(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            # Normalize operation string
            operation = data.get("operation", "").strip().lower()

            matrixA = parse_matrix(data.get("matrixA"))
            if matrixA is None:
                return JsonResponse({"error": "Invalid matrixA format"}, status=400)

            # For operations that require matrixB: add, subtract, multiply
            matrixB = None
            if operation in ["add", "subtract", "multiply"]:
                matrixB = parse_matrix(data.get("matrixB"))
                if matrixB is None:
                    return JsonResponse({"error": "Invalid matrixB format"}, status=400)

            if operation == "add":
                if matrixA.shape != matrixB.shape:
                    return JsonResponse({"error": "Matrix dimensions must match for addition"}, status=400)
                result_matrix = np.add(matrixA, matrixB)
            elif operation == "subtract":
                if matrixA.shape != matrixB.shape:
                    return JsonResponse({"error": "Matrix dimensions must match for subtraction"}, status=400)
                result_matrix = np.subtract(matrixA, matrixB)
            elif operation == "scalar":
                scalar = data.get("scalar")
                if scalar is None:
                    return JsonResponse({"error": "Missing scalar value"}, status=400)
                try:
                    scalar = float(scalar)
                except ValueError:
                    return JsonResponse({"error": "Invalid scalar value"}, status=400)
                result_matrix = np.multiply(matrixA, scalar)
            elif operation == "multiply":
                # Check if the number of columns in matrixA equals the number of rows in matrixB
                if matrixA.shape[1] != matrixB.shape[0]:
                    return JsonResponse({"error": "Matrix dimensions do not allow multiplication"}, status=400)
                result_matrix = np.matmul(matrixA, matrixB)
            elif operation == "gauss":
                result_matrix = gaussian_elimination(matrixA)
            elif operation == "jordan":
                result_matrix = gauss_jordan_elimination(matrixA)
            else:
                return JsonResponse({"error": "Invalid operation"}, status=400)

            return JsonResponse({"result": result_matrix.tolist()}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Invalid request"}, status=400)

def parse_matrix(matrix_str):
    """ Convert a string like '2,1,-1;1,3,2;1,-1,2' into a NumPy array """
    try:
        if not matrix_str:
            return None
        matrix = [list(map(float, row.split(","))) for row in matrix_str.split(";")]
        return np.array(matrix)
    except ValueError:
        return None

def gaussian_elimination(matrix):
    """ Perform Gaussian elimination (convert to row echelon form) """
    A = np.array(matrix, dtype=float)
    rows, cols = A.shape
    for i in range(min(rows, cols)):
        max_row = i + np.argmax(np.abs(A[i:, i]))
        if A[max_row, i] == 0:
            continue
        A[[i, max_row]] = A[[max_row, i]]
        A[i] /= A[i, i]
        for j in range(i+1, rows):
            A[j] -= A[i] * A[j, i]
    return A.tolist()

def gauss_jordan_elimination(matrix):
    """ Perform Gauss-Jordan elimination (convert to reduced row echelon form) """
    A = np.array(matrix, dtype=float)
    rows, cols = A.shape
    for i in range(min(rows, cols)):
        max_row = i + np.argmax(np.abs(A[i:, i]))
        if A[max_row, i] == 0:
            continue
        A[[i, max_row]] = A[[max_row, i]]
        A[i] /= A[i, i]
        for j in range(rows):
            if j != i:
                A[j] -= A[i] * A[j, i]
    return A.tolist()
