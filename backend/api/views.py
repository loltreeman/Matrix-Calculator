import json
import numpy as np
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

ALLOWED_OPERATIONS = ["add", "subtract", "multiply", "gauss"]

@csrf_exempt
def calculate_matrix(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            matrixA = data.get("matrixA")
            matrixB = data.get("matrixB", None)  # Needed for add/subtract/multiply
            operation = data.get("operation")

            if operation not in ALLOWED_OPERATIONS:
                return JsonResponse({"error": "Invalid operation"}, status=400)

            # Convert matrix strings to NumPy arrays
            matrixA = parse_matrix(matrixA)
            if matrixA is None:
                return JsonResponse({"error": "Invalid matrix format"}, status=400)

            if operation in ["add", "subtract", "multiply"]:
                if not matrixB:
                    return JsonResponse({"error": "Matrix B is required for this operation"}, status=400)
                matrixB = parse_matrix(matrixB)
                if matrixB is None:
                    return JsonResponse({"error": "Invalid matrix format"}, status=400)

            # Perform the requested operation
            if operation == "add":
                result = matrixA + matrixB
            elif operation == "subtract":
                result = matrixA - matrixB
            elif operation == "multiply":
                result = np.dot(matrixA, matrixB)
            elif operation == "gauss":
                result = gaussian_elimination(matrixA)
            else:
                return JsonResponse({"error": "Operation not implemented"}, status=400)

            return JsonResponse({"result": result.tolist()})

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

    return JsonResponse({"error": "Invalid request"}, status=400)


def parse_matrix(matrix_str):
    """
    Convert a semicolon-separated matrix string into a NumPy array.
    Example: "2,1,-1;1,3,2;1,-1,2" -> np.array([[2,1,-1],[1,3,2],[1,-1,2]])
    """
    try:
        matrix = [[float(num) for num in row.split(",")] for row in matrix_str.split(";")]
        return np.array(matrix)
    except ValueError:
        return None


def gaussian_elimination(matrix):
    """
    Perform Gaussian elimination (row echelon form).
    """
    A = matrix.astype(float)
    rows, cols = A.shape

    for i in range(min(rows, cols)):
        # Find pivot
        max_row = np.argmax(abs(A[i:, i])) + i
        A[[i, max_row]] = A[[max_row, i]]  # Swap rows

        # Normalize pivot row
        A[i] /= A[i, i]

        # Eliminate below
        for j in range(i + 1, rows):
            A[j] -= A[j, i] * A[i]

    return A
