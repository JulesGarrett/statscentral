from django.shortcuts import render
from django.db import connection
# from cities.models import Cities, Reviews
from cities.models import CityReviews
from cities.forms import CreateReviewForm
from account.models import Account

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

	user = request.user
    
	form = CreateReviewForm(request.POST or None)
	if form.is_valid():
		obj = form.save(commit=False)
		author = Account.objects.filter(email=request.user.email).first()
		obj.author = author
		obj.save()

	context['form'] = form

	return render(request, 'cities/create_review.html', context)


def edit_review_view(request, slug):

	context = {}
	user = request.user

	review = get_object_or_404(BlogPost, slug=slug)
	if request.POST:
		form = UpdateBlogPostForm(request.POST or None, request.FILES or None, instance=blog_post)
		if form.is_valid():
			obj = form.save(commit=False)
			obj.save()
			context['success_message'] = "Updated"
			blog_post = obj

	form = UpdateBlogPostForm(
			initial={
					"title": blog_post.title,
					"body": blog_post.body,
					"image": blog_post.image,
				}
			)
	context['form'] = form

	return render(request, 'blog/edit_blog.html', context)
