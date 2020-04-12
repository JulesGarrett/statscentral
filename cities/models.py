from django.db import models
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.conf import settings
from django.db.models.signals import post_delete
from django.dispatch import receiver


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
	City 					= models.CharField(max_length=50, null=False, blank=False)
	Comments 				= models.TextField(max_length=1000)
	Rating		 			= models.IntegerField(blank=False, null=False)
	author 					= models.CharField(max_length=30, null=False, blank=False)
	slug 					= models.SlugField(blank=True, unique=True)

	def __str__(self):
		return str(self.City) + str(self.author)

@receiver(post_delete, sender=Reviews)

def pre_save_review_receiver(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = slugify(instance.author + "-" + instance.City)

pre_save.connect(pre_save_review_receiver, sender=Reviews)
