from django.db import models

# Create your models here.
class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birthday = models.DateField()
    favorite_activities = models.TextField()
    email = models.EmailField(max_length = 254)
    education = (
    	('NONE', 'None'),
    	('HS', 'high school'),
    	('UG', 'undergraduate'),
    	('MS', 'masters'),
    	('PhD', 'phd')
    )

class Article(models.Model):
    title = models.CharField(max_length=150)
    published_date = models.DateField()
    content = models.TextField()
    writer = models.ForeignKey(Author)
