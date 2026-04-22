from rest_framework import serializers
from .models import Earthquake
from .utils.geocode import reverse_geocode
from django.core.cache import cache


class EarthquakeSerializer(serializers.ModelSerializer):
    location = serializers.SerializerMethodField()

    class Meta:
        model = Earthquake
        fields = "__all__"  # or explicitly list + "location"

    def get_location(self, obj):
        lat = round(obj.latitude, 3)
        lng = round(obj.longitude, 3)

        cache_key = f"geo:{lat}:{lng}"

        # 1. Check cache first
        cached = cache.get(cache_key)
        if cached:
            return cached

        # 2. Call geocode
        location = reverse_geocode(lat, lng)

        if location:
            cache.set(cache_key, location, timeout=86400)  # 24 hours
            return location

        return "Unknown location"