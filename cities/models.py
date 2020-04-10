from django.db import models

class Cities(models.Model):
	Zip_ID 					= models.IntegerField(blank=True, null=True)
	ZipCode 				= models.IntegerField(blank=True, null=True)
	CityID					= models.IntegerField(blank=True, null=True)
	City 					= models.CharField(max_length=50, null=False, blank=False)
	Latitude				= models.IntegerField(blank=True, null=True)
	Longitude 				= models.IntegerField(blank=True, null=True)
	Population				= models.IntegerField(blank=True, null=True)

	def __str__(self):
		return self.City

class Reviews(models.Model):
	username				= models.CharField(max_length=30, blank=False, null=False)
	City					= models.CharField(max_length=50, null=False, blank=False)
	Rating					= models.IntegerField(blank=True, null=True)
	Comments				= models.TextField(max_length=2000, null=True, blank=True)

	def __str__(self):
		return self.username +"_" +self.City
