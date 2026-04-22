from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Earthquake
from .serializers import EarthquakeSerializer
# from .utils.geocode import get_location_name
import requests



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




@api_view(["GET"])
def get_location(request):
    lat = request.GET.get("lat")
    lng = request.GET.get("lng")

    if not lat or not lng:
        return Response({"error": "lat/lng required"}, status=400)

    location = reverse_geocode(lat, lng)

    if not location:
        return Response({"error": "Geocoding failed"}, status=500)

    return Response({
        "latitude": lat,
        "longitude": lng,
        "location": location
    })

@api_view(["GET"])
def live_earthquakes(request):
    url = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_day.geojson"

    try:
        res = requests.get(url)
        data = res.json()

        earthquakes = []

        for feature in data["features"]:
            props = feature["properties"]
            coords = feature["geometry"]["coordinates"]

            earthquakes.append({
                "id": feature["id"],
                "magnitude": props["mag"],
                "place": props["place"],
                "time": props["time"],
                "longitude": coords[0],
                "latitude": coords[1],
            })

        return Response(earthquakes)

    except Exception as e:
        return Response({"error": str(e)}, status=500)


# Create your views here.
