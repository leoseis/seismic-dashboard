from django.urls import path
from . import views

urlpatterns = [
    path("earthquakes/", views.earthquakes_list),
    path("earthquakes/latest/", views.latest_earthquakes),
    path("earthquakes/filter/", views.filter_earthquakes),
    path("location/", views.get_location),
    path("live-earthquakes/", views.live_earthquakes),  
]