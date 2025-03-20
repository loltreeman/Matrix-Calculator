from django.urls import path
from .views import calculate_matrix
from django.http import JsonResponse

def matrix_home(request):
    return JsonResponse({"message": "Welcome to the Matrix API!"})

urlpatterns = [
    path("", matrix_home, name="matrix_home"),  # Handles "/matrix/"
    path("calculate/", calculate_matrix, name="calculate_matrix"),  # Handles "/matrix/calculate/"
]
