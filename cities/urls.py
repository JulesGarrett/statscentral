from django.urls import path
from cities.views import search_cities, create_review, edit_review

app_name = 'cities'

urlpatterns = [
    path('search', search_cities, name="search"),
    path('create_review', create_review, name="create_review"),
    path('edit_review', edit_review, name="edit_review")
 ]
