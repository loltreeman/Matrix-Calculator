import json
import numpy as np  
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

ALLOWED_OPERATIONS = ["add", "subtract", "multiply", "scalar", "gauss", "jordan"]

@csrf_exempt  
def calculate_matrix(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            operation = data.get("operation", "").strip().lower()
            if operation not in ALLOWED_OPERATIONS:
                return JsonResponse({"error": "Invalid operation"}, status=400)

            # This is to parse MatrixA
            matrixA = parse_matrix(data.get("matrixA"))
            if matrixA is None:
                return JsonResponse({"error": "Invalid matrixA format"}, status=400)

            # For operations that require matrixB (add, subtract, multiply), parse it
            matrixB = None
            if operation in ["add", "subtract", "multiply"]:
                matrixB = parse_matrix(data.get("matrixB"))
                if matrixB is None:
                    return JsonResponse({"error": "Invalid matrixB format"}, status=400)
                if matrixA.shape != matrixB.shape:
                    return JsonResponse({"error": "Matrix dimensions must match for addition/subtraction"}, status=400)

            if operation == "scalar":
                scalar = data.get("scalar")
                if scalar is None:
                    return JsonResponse({"error": "Missing scalar value"}, status=400)
                try:
                    scalar = float(scalar)
                except ValueError:
                    return JsonResponse({"error": "Invalid scalar value"}, status=400)
                result_matrix = np.multiply(matrixA, scalar)
            elif operation == "add":
                result_matrix = np.add(matrixA, matrixB)
            elif operation == "subtract":
                result_matrix = np.subtract(matrixA, matrixB)
            elif operation == "multiply":
                if matrixA.shape[1] != matrixB.shape[0]:
                    return JsonResponse({"error": "Matrix dimensions do not allow multiplication"}, status=400)
                result_matrix = np.matmul(matrixA, matrixB)
            elif operation in ["gauss", "jordan"]:
                if data.get("matrixB"):
                    matrixB = parse_matrix(data.get("matrixB"))
                    if matrixB is None:
                        return JsonResponse({"error": "Invalid matrixB format"}, status=400)
                    aug_matrix = np.hstack((matrixA, matrixB))
                else:
                    aug_matrix = matrixA

                aug_list = aug_matrix.tolist()
                if operation == "gauss":
                    ref = gaussian_elimination(aug_list)
                    solution_status = determine_solution_status(ref)
                    result_matrix = ref
                else:
                    rref = gauss_jordan_elimination(aug_list)
                    solution_status = determine_solution_status(rref)
                    result_matrix = rref

                return JsonResponse({
                    "result": result_matrix,
                    "solution_status": solution_status
                }, status=200)
            else:
                return JsonResponse({"error": "Invalid operation"}, status=400)

            return JsonResponse({"result": np.array(result_matrix, dtype=float).tolist()}, status=200)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid request"}, status=400)


def parse_matrix(matrix_str):
    try:
        if not matrix_str:
            return None
        matrix_str = matrix_str.rstrip(";\n ")
        matrix = [list(map(float, row.split(","))) for row in matrix_str.split(";") if row.strip()]
        return np.array(matrix, dtype=float)
    except ValueError:
        return None


def gaussian_elimination(matrix):
    matrix = np.array(matrix, dtype=float)
    m, n = matrix.shape
    
    for i in range(min(m, n - 1)):
        max_row = i + np.argmax(np.abs(matrix[i:, i]))
        if matrix[max_row, i] == 0:
            continue
        matrix[[i, max_row]] = matrix[[max_row, i]]
        matrix[i] = matrix[i] / matrix[i, i]
        for j in range(i + 1, m):
            matrix[j] -= matrix[j, i] * matrix[i]
    return matrix.tolist()


def gauss_jordan_elimination(matrix):
    matrix = np.array(gaussian_elimination(matrix), dtype=float)
    m, n = matrix.shape
    for i in range(m - 1, -1, -1):
        if matrix[i, i] == 0:
            continue
        for j in range(i - 1, -1, -1):
            matrix[j] -= matrix[j, i] * matrix[i]
    return matrix.tolist()

# This is to tell us if a matrix has infinite, one unique solution, or no solution.
def determine_solution_status(aug_matrix):
    aug_matrix = np.array(aug_matrix, dtype=float)
    m, n = aug_matrix.shape
    num_vars = n - 1
    pivot_count = 0
    for row in aug_matrix:
        if np.all(row[:-1] == 0) and row[-1] != 0:
            return "none"
        if np.any(row[:-1] != 0):
            pivot_count += 1
    if pivot_count < num_vars:
        return "infinite"
    else:
        return "unique"
