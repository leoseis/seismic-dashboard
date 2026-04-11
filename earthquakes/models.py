from django.db import models

class Earthquake(models.Model):

    magnitude = models.FloatField()
    depth = models.FloatField()

    latitude = models.FloatField()
    longitude = models.FloatField()

    location = models.CharField(max_length=255)

    time = models.DateTimeField()

    source = models.CharField(max_length=50, default="USGS")

    def __str__(self):
        return f"M{self.magnitude} - {self.location}"
