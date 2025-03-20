import json
import numpy as np  # Make sure to install: pip install numpy
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def calculate_matrix(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            matrixA = data.get("matrixA")
            matrixB = data.get("matrixB")
            operation = data.get("operation")

            # Convert string input to NumPy arrays
            matrixA = np.array([list(map(int, row.split(","))) for row in matrixA.split(";")])
            matrixB = np.array([list(map(int, row.split(","))) for row in matrixB.split(";")])

            if operation == "add":
                result_matrix = matrixA + matrixB
            elif operation == "subtract":
                result_matrix = matrixA - matrixB
            elif operation == "scalar":
                result_matrix = 2 * matrixA  # Example: Multiply by 2
            else:
                return JsonResponse({"error": "Invalid operation"}, status=400)

            # Convert NumPy array to a regular list for JSON serialization
            result_list = result_matrix.tolist()

            return JsonResponse({"result": result_list}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Invalid request"}, status=400)
