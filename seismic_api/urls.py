from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

urlpatterns = [
    path('admin/', admin.site.urls),
   path('api/', include('earthquakes.urls')),
    # optional health check
    path('', lambda request: JsonResponse({"status": "API running"})),
]