from django.db import models

# Create your models here.
class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.Charfield(max_lengths=100)
    birthday = models.Datefield(auto_now=False, auto_now_add=False)
    favorite_activies = models.Textfield()
    email = models.Emailfield(max_length=254)
    education = models.Charfield(max_length=100, choices=("None", "high school", "undergraduate", "masters", "phd"), default='1')


class Article(models.Model):
    title = models.CharField(max_length=150)
    published_date = models.Datefield(auto_now=Flase, auto_now_add=False)
    content = models.TextField()
    writer = models.ForeignKey('self', NULL = True, on_delete=SET_NULL)

    
