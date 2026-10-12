from django.urls import path
from .views import waste_list, waste_detail

urlpatterns = [
    path("waste/", waste_list, name="waste-list"),
    path("waste/<int:pk>/", waste_detail, name="waste-detail"),
]