from rest_framework.decorators import api_view
from rest_framework.response import Response
import numpy as np

@api_view(['POST'])
def calculate_matrix(request):
    data = request.data
    matrixA = np.array([list(map(float, row.split(','))) for row in data['matrixA'].split(';')])
    matrixB = np.array([list(map(float, row.split(','))) for row in data['matrixB'].split(';')]) if 'matrixB' in data else None
    operation = data.get('operation')

    if operation == 'add' and matrixB is not None:
        result = matrixA + matrixB
    elif operation == 'subtract' and matrixB is not None:
        result = matrixA - matrixB
    elif operation == 'scalar':
        scalar = float(data['scalar'])
        result = matrixA * scalar
    else:
        return Response({"error": "Invalid operation"}, status=400)

    return Response({"result": result.tolist()})
