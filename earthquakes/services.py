import requests
from .models import Earthquake
from datetime import datetime


USGS_URL = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_day.geojson"


def fetch_earthquakes():

    response = requests.get(USGS_URL)
    data = response.json()

    for eq in data["features"]:

        props = eq["properties"]
        coords = eq["geometry"]["coordinates"]

        Earthquake.objects.create(
            magnitude=props["mag"] or 0,
            location=props["place"],
            time=datetime.fromtimestamp(props["time"] / 1000),
            longitude=coords[0],
            latitude=coords[1],
            depth=coords[2],
        )