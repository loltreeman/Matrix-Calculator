from django.urls import path
from .views import calculate_matrix

urlpatterns = [
    path("calculate/", calculate_matrix, name="calculate_matrix"),
]
