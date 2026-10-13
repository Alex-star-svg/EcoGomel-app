from django.urls import path

from .views import points_list, waste_list


urlpatterns = [
    path("waste/", waste_list),
    path("points/", points_list),
]