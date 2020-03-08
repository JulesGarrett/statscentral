from django.shortcuts import render, HttpResponse
from django.db import connection
from accounts.models import City1

# Create your views here.
def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]

def get_db_data():
    with connection.cursos() as cursor:
        cursor.execute("SELECT CityName FROM Cities;")
        result = cursor.fetchall()
        return result




def home(request):
    db_results = City1.objects.get(id=1)    
    return render(request, 'index.html', {'cities':db_results})
