from django.db import models


class Cities(models.Model):
	Zip_ID 					= models.IntegerField(blank=True, null=True)
	ZipCode 				= models.IntegerField(blank=True, null=True)
	CityID					= models.IntegerField(blank=True, null=True)
	City 					= models.CharField(max_length=50, null=False, blank=False, primary_key=True)
	Latitude				= models.IntegerField(blank=True, null=True)
	Longitude 				= models.IntegerField(blank=True, null=True)
	Population				= models.IntegerField(blank=True, null=True)

	def __str__(self):
		return self.City
