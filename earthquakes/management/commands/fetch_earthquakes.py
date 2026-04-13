import requests
from django.core.management.base import BaseCommand
from earthquakes.models import Earthquake
from datetime import datetime


USGS_URL = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_day.geojson"


class Command(BaseCommand):

    help = "Fetch earthquake data from USGS"

    def handle(self, *args, **kwargs):

        self.stdout.write("Fetching earthquake data...")

        response = requests.get(USGS_URL)
        data = response.json()

        count = 0

        for eq in data["features"]:

            props = eq["properties"]
            coords = eq["geometry"]["coordinates"]

            magnitude = props["mag"]
            location = props["place"]
            timestamp = props["time"]

            longitude = coords[0]
            latitude = coords[1]
            depth = coords[2]

            # convert timestamp
            time = datetime.fromtimestamp(timestamp / 1000)

            usgs_id = eq["id"]

            earthquake, created = Earthquake.objects.update_or_create(
                usgs_id=usgs_id,
                defaults={
                    "magnitude": magnitude or 0,
                    "location": location,
                    "time": time,
                    "longitude": longitude,
                    "latitude": latitude,
                    "depth": depth,
                }
            )

            if created:
                count += 1

        self.stdout.write(self.style.SUCCESS(
            f"{count} earthquakes saved to database"
        ))