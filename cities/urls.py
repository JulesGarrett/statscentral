from django.urls import path
from cities.views import search_cities#, city_details

app_name = 'cities'

urlpatterns = [
    path('search', search_cities, name="search"),
    # path('city_details', city_details, name="city_details")
 ]
