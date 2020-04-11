from django.urls import path
from cities.views import search_cities

app_name = 'cities'

urlpatterns = [
    path('search', search_cities, name="search"),
 ]
