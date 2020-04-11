from django.db import models
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.conf import settings
from django.db.models.signals import post_delete
from django.dispatch import receiver
from datetime import datetime


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


class CityReviews(models.Model):
	City 					= models.CharField(max_length=50, null=False, blank=False)
	Comments 				= models.TextField(max_length=5000, null=True, blank=True)
	Rating		 			= models.IntegerField(blank=False, null=False)
	date_added 				= models.DateTimeField(auto_now_add=True, verbose_name="date published")
	date_updated 			= models.DateTimeField(auto_now=True, verbose_name="date updated")
	author 					= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	slug 					= models.SlugField(blank=True, unique=True)
	# give options
	OVERALLCITY = 1
	SCHOOL = 2
	MILITARY = 3
	REVIEW_TYPE = ((OVERALLCITY, 'City'),(SCHOOL, 'School'),(MILITARY, 'Military'),)
	ReviewType 				= models.PositiveSmallIntegerField(choices=REVIEW_TYPE, null=False, blank=False, default='1')

	def __str__(self):
		return str(self.City) + str(author)

@receiver(post_delete, sender=CityReviews)

def pre_save_review_receiver(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = slugify(instance.author.username + "-" + instance.City)

pre_save.connect(pre_save_review_receiver, sender=CityReviews)
