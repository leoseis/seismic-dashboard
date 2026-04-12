from django.contrib import admin

# Register your models here.from django.contrib import admin
from .models import Earthquake


@admin.register(Earthquake)
class EarthquakeAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "magnitude",
        "depth",
        "location",
        "latitude",
        "longitude",
        "time",
    )

    list_filter = ("magnitude", "time")

    search_fields = ("location",)

    ordering = ("-time",)
