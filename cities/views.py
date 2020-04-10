from django.shortcuts import render
from cities.models import Cities, Reviews

# Create your views here.
def home_screen_view(request):
    context = {}
    return render(request, "cities/home.html", context)

def search_cities(request):
    context = {}
    context['cities'] = ["Kanas City", "New York", "Boston"]
    return render(request, 'cities/search.html', context)
