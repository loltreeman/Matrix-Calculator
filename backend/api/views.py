import json
import numpy as np  
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def calculate_matrix(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            operation = data.get("operation")

            matrixA = parse_matrix(data.get("matrixA"))
            if matrixA is None:
                return JsonResponse({"error": "Invalid matrixA format"}, status=400)

            matrixB = None
            if operation in ["add", "subtract"]:
                matrixB = parse_matrix(data.get("matrixB"))
                if matrixB is None:
                    return JsonResponse({"error": "Invalid matrixB format"}, status=400)

                if np.array(matrixA).shape != np.array(matrixB).shape:
                    return JsonResponse({"error": "Matrix dimensions must match for addition/subtraction"}, status=400)

            if operation == "add":
                result_matrix = np.add(matrixA, matrixB)
            elif operation == "subtract":
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
