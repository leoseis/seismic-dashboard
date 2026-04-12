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

# Create your views here.
