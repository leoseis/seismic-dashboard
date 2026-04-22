import requests
from django.conf import settings

OPENCAGE_URL = "https://api.opencagedata.com/geocode/v1/json"


def reverse_geocode(lat, lng):
    """
    Convert latitude & longitude into a human-readable location.
    """

    params = {
        "q": f"{lat},{lng}",
        "key": settings.OPENCAGE_API_KEY,
        "no_annotations": 1,
        "language": "en"
    }

    try:
        response = requests.get(OPENCAGE_URL, params=params, timeout=5)

        if response.status_code != 200:
            return None

        data = response.json()

        if not data.get("results"):
            return None

        result = data["results"][0]
        components = result.get("components", {})

        # ✅ Correctly inside try block
        city = (
            components.get("city")
            or components.get("town")
            or components.get("village")
            or components.get("suburb")
            or components.get("county")
        )

        country = components.get("country")

        if city and country:
            return f"{city}, {country}"

        return country or "Unknown location"

    except requests.RequestException:
        return None