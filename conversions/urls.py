from django.urls import path, include

from . import api as conversions_apis

urlpatterns = [
    path('convert/', conversions_apis.conversion_api, name="conversion-api")
]
