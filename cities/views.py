from django.shortcuts import render, redirect, get_object_or_404
from django.db import connection
# from cities.models import Cities, Reviews
from cities.models import CityReviews
from cities.forms import CreateReviewForm, UpdateReviewForm
from account.models import Account
from wordcloud import WordCloud, STOPWORDS


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

# old function that was used in old deliverable
def get_cities_sql():
    with connection.cursor() as cursor:
        cursor.execute("SELECT City, Sum(Population) AS Population FROM `cities_cities` group by City Limit 10;")
        cities = dictfetchall(cursor)
    return cities

# query that is used to search for cities by name
def search_city_match(query=None):
    with connection.cursor() as cursor:
        cursor.execute("SELECT City_ID as CityID, City, State FROM C_US_MilitaryCities WHERE City LIKE '%" + str(query)+ "%' Order by length(City), City, State Limit 25")
        cities = dictfetchall(cursor)
    return cities

# need to change to be large query with tons of joins
def get_city_by_id(id=None):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM C_US_MilitaryCities WHERE CITY_ID = "+str(id))
        city = dictfetchall(cursor)
    return city[0]


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


def detail_city(request, id):
    context = {}
    city = get_city_by_id(id)
    context['city'] = city
    return render(request, 'cities/city_detail.html', context)


############### REVIEW ###############
def create_review(request):
    context = {}
    user = request.user
    if request.POST:
        form = CreateReviewForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            author = Account.objects.filter(email=request.user.email).first()
            obj.author = author
            obj.save()
    else:
        form = CreateReviewForm()
    context['form'] = form
    return render(request, 'cities/create_review.html', context)


def detail_review(request, slug):
    context = {}
    review = get_object_or_404(CityReviews, slug=slug)
    context['review'] = review
    return render(request, 'cities/detail_review.html', context)


def delete_review(request, slug):
    context = {}
    obj = get_object_or_404(CityReviews, slug=slug)
    context['object'] = obj
    if request.POST:
        obj.delete()
        return redirect('home')
    return render(request, "cities/delete_review.html", context)


def edit_review(request, slug):
    context = {}
    user = request.user

    review = get_object_or_404(CityReviews, slug=slug)
    if request.POST:
        form = UpdateReviewForm(request.POST or None, instance=review)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            context['success_message'] = "Updated Review for "+str(review.City)
            review = obj

    form = UpdateReviewForm(
			initial={
					"Comments": review.Comments,
					"Rating": review.Rating,
				}
			)
    context['form'] = form
    context['city'] = review.City
    return render(request, 'cities/edit_review.html', context)

def city_match(request):
    context = {}
    return render(request, "cities/city_match.html", context)
