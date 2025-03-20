import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt  # Disable CSRF for now (use Django REST Framework for production)
def calculate_matrix(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            matrixA = data.get("matrixA")
            matrixB = data.get("matrixB")
            operation = data.get("operation")

            # Dummy result for testing
            result = {
                "matrixA": matrixA,
                "matrixB": matrixB,
                "operation": operation,
                "output": "Calculated result here",
            }

            return JsonResponse({"result": result}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Invalid request"}, status=400)
