from django.shortcuts import render
from django.db import connection
# from cities.models import Cities, Reviews

######################################
#         Helper Functions           #
######################################

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

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


######################################
#          View Functions            #
######################################

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

def create_review(request):
    context = {}
    return render(request, "cities/create_review.html", context)
