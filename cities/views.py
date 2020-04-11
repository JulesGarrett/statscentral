from django.shortcuts import render
from django.db import connection
# from cities.models import Cities, Reviews

# Create your views here.
def home_screen_view(request):
    context = {}
    return render(request, "cities/home.html", context)

def search_cities(request):
    context = {}
    context['cities'] = get_cities_sql()
    return render(request, 'cities/search.html', context)

def get_cities_sql():
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM cities_cities WHERE City NOT NULL LIMIT 10;")
        cites = dictfetchall(cursor)	#[{'Game_ID': 1, 'Description': "...", Image:"...", ...}, {'Game_ID': 2, 'Description': "...", Image:"..."}...]
    return cites

def create_review(request):
    context = {}
    return render(request, 'cities/home.html')
