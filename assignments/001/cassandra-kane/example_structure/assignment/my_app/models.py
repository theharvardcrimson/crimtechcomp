from django.db import models

# Create your models here.
class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birthday = models.DateField()
    favorite_activities = models.TextField()
    email = models.EmailField()
    education = models.CharField(choices=["none", "high school", "undergraduate", "masters", "phd"])

class Article(models.Model):
    title = models.CharField(max_length=150)
    published_date = models.DateField()
    content = models.TextField()
    writer = models.ForeignKey('Author', on_delete=models.PROTECT)