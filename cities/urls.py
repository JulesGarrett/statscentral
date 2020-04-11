from django.urls import path
from cities.views import search_cities, review

app_name = 'cities'

urlpatterns = [
    path('search', search_cities, name="search"),
    path('review', review, name="review"),
 ]



# def search_city_match(query=None):
#     all_cities = []
#     cities = Cities.objects.filter(
#     			Q(City__contains=query)
#     			).distinct()
#     for city in cities:
#         all_cities.append(city)
#     return all_cities
