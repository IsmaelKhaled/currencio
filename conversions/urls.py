from django.urls import path, include
from rest_framework.authtoken import views

from . import api as conversions_apis

urlpatterns = [
    path('convert/', conversions_apis.conversion_api, name="conversion-api")
]


urlpatterns += [
    path('api-token-auth/', views.obtain_auth_token)
]
