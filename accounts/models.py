from django.db import models

# Create your models here.
class City1(models.Model):
    name = models.CharField(db_column='CityName', max_length=200)
    population = models.IntegerField(db_column='Population')
    zipcode = models.IntegerField(db_column='Zip')
    state = models.CharField(db_column='State', max_length=20)
    lat = models.FloatField(db_column='Latitude')
    lon = models.FloatField(db_column='Longitude')
