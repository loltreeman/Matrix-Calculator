import json
import numpy as np  
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt  # Disable CSRF for now (for production, use proper CSRF handling)
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
                if matrixA.shape[1] != matrixB.shape[0]:
                    return JsonResponse({"error": "Matrix dimensions do not allow multiplication"}, status=400)
                result_matrix = np.matmul(matrixA, matrixB)
            elif operation == "gauss":
                result_matrix = gaussian_elimination(matrixA)
            elif operation == "jordan":
                result_matrix = gauss_jordan_elimination(matrixA)
            else:
                return JsonResponse({"error": "Invalid operation"}, status=400)

            # Convert the NumPy array result to a list for JSON serialization.
            return JsonResponse({"result": np.array(result_matrix, dtype=float).tolist()}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid request"}, status=400)


def parse_matrix(matrix_str):
    """Convert a string like '2,1,-1;1,3,2;1,-1,2' into a NumPy array."""
    try:
        if not matrix_str:
            return None
        matrix = [list(map(float, row.split(","))) for row in matrix_str.split(";")]
        return np.array(matrix, dtype=float)
    except ValueError:
        return None


def gaussian_elimination(matrix):
    """
    Perform Gaussian elimination (convert to row echelon form) and return a NumPy array.
    """
    A = np.array(matrix, dtype=float)  # Ensure input is a NumPy array
    rows, cols = A.shape
    for i in range(min(rows, cols)):
        # Find the pivot row
        max_row = i + np.argmax(np.abs(A[i:, i]))
        if A[max_row, i] == 0:
            continue
        # Swap the current row with the pivot row
        A[[i, max_row]] = A[[max_row, i]]
        # Normalize the pivot row
        A[i] = A[i] / A[i, i]
        # Eliminate below
        for j in range(i + 1, rows):
            A[j] = A[j] - A[j, i] * A[i]
    return A  # Return as a NumPy array


def gauss_jordan_elimination(matrix):
    """
    Perform Gauss-Jordan elimination (convert to reduced row echelon form) and return a NumPy array.
    """
    A = gaussian_elimination(matrix)
    rows, cols = A.shape
    # Eliminate above the pivot
    for i in range(rows - 1, -1, -1):
        for j in range(i - 1, -1, -1):
            A[j] = A[j] - A[j, i] * A[i]
    return A  # Return as a NumPy array
