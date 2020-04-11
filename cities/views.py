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
    if request.GET:
        query = request.GET['q']
        context['query'] = str(query)
        context['cities'] = search_city_match(query)
    return render(request, 'cities/search.html', context)


def get_cities_sql():
    with connection.cursor() as cursor:
        cursor.execute("SELECT City, Sum(Population) AS Population FROM `cities_cities` group by City Limit 10;")
        cities = dictfetchall(cursor)
    return cities

def search_city_match(query=None):
    with connection.cursor() as cursor:
        cursor.execute("SELECT City, Sum(Population) AS Population FROM `cities_cities` WHERE City LIKE '%" +str(query)+ "%' group by City Limit 10")
        cities = dictfetchall(cursor)
    return cities

# def get_one_city(city_name):
#     with connection.cursor() as cursor:
#         cursor.execute("SELECT City, Sum(Population) AS Population FROM `cities_cities` WHERE City = "+str(city_name)+" group by City Limit 10;")
#         cites = dictfetchall(cursor)
#     return cites


# def city_details(request, city_name):
#     context = {}
#     city = get_one_city(city_name)
#     if not city:
#         raise Http404("City does not exist")
#     context['city'] = city
#     context['user'] = request.user
#     return render(request, "cities/city_details.html", context)
