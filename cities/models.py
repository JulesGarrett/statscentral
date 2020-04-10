from django.db import models


class Cities(models.Model):
	State_ID 				= models.IntegerField(blank=True, null=True, primary_key=True)
	City 					= models.CharField(max_length=50, null=False, blank=False, primary_key=True)
	State		 			= models.CharField(max_length=50, null=False, blank=False)

	def __str__(self):
		return self.City
