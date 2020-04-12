from django.urls import path
from cities.views import search_cities, create_review, edit_review, detail_review, delete_review

app_name = 'cities'

urlpatterns = [
    path('search', search_cities, name="search"),
    path('create_review', create_review, name="create_review"),
    path('<slug>/', detail_review, name="detail"),
    path('<slug>/edit/', edit_review, name="edit_review"),
    path('<slug>/delete/', delete_review, name="delete_review")
 ]
