from django.shortcuts import render

# Create your views here.
def home_screen_view(request):
    context = {}
    return render(request, "cities/home.html", context)
