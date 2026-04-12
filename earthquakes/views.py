from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Earthquake
from .serializers import EarthquakeSerializer


@api_view(["GET"])
def earthquakes_list(request):

    earthquakes = Earthquake.objects.all().order_by("-time")[:100]

    serializer = EarthquakeSerializer(earthquakes, many=True)

    return Response(serializer.data)


@api_view(["GET"])
def latest_earthquakes(request):

    earthquakes = Earthquake.objects.order_by("-time")[:20]

    serializer = EarthquakeSerializer(earthquakes, many=True)

    return Response(serializer.data)


@api_view(["GET"])
def filter_earthquakes(request):

    min_mag = request.GET.get("min_mag")
    max_mag = request.GET.get("max_mag")

    earthquakes = Earthquake.objects.all()

    if min_mag:
        earthquakes = earthquakes.filter(magnitude__gte=min_mag)

    if max_mag:
        earthquakes = earthquakes.filter(magnitude__lte=max_mag)

    serializer = EarthquakeSerializer(earthquakes, many=True)

    return Response(serializer.data)

# Create your views here.
