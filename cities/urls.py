from django.urls import path
from cities.views import search_cities

app_name = 'blog'

urlpatterns = [
    path('search', search_cities, name="search"),
    path('review', create_review, name="make_review"),
 ]
