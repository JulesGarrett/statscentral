from django.urls import path
from cities.views import search_cities, create_review

app_name = 'cities'

urlpatterns = [
    path('search', search_cities, name="search"),
    path('create_review', create_review, name="create_review"),
 ]
