from django.db import models

# Create your models here.
class Author(models.Model):
	first_name = models.CharField(max_length=100)
	last_name = models.CharField(max_length=100)
	birthday = models.DateField()
	favorite_activities = models.TextField(max_length=254)
	email = models.EmailField()
	education = models.CharField(max_length=150, choices=(
		("NONE", "none"), 
		("HIGH_SCHOOL", "high school"), 
		("UNDERGRADUATE", "undergraduate"),
		("MASTERS", "masters"),
		("PHD", "phd"))
	)

class Article(models.Model):
	title = models.CharField(max_length=150)
	published_date = models.DateField()
	content = models.TextField(max_length=254)
	writer = models.ForeignKey('Author', on_delete=models.CASCADE)
