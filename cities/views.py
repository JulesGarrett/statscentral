from django.shortcuts import render
from django.db import connection
# from cities.models import Cities, Reviews

# Create your views here.
def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def home_screen_view(request):
    context = {}
    return render(request, "cities/home.html", context)

def search_cities(request):
    context = {}
    context['cities'] = get_cities_sql()
    return render(request, 'cities/search.html', context)

def get_cities_sql():
    with connection.cursor() as cursor:
        cursor.execute("SELECT City, Sum(Population) AS Population FROM `cities_cities` group by City Limit 10;")
        cites = dictfetchall(cursor)
    return cites

def city_details(request, city_name):
    context = {}
    with connection.cursor() as cursor:
        cursor.execute("SELECT City, Sum(Population) AS Population FROM `cities_cities` group by City Having City = "+str(city_name))
        city = dictfetchall(cursor)
        context['city'] = city
    return render(request, 'cities/city_details.html', context)
