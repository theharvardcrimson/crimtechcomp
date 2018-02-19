from django.db import models

# Create your models here.
class Author(models.Model):
    NONE = "None"
    HIGH_SCHOOL = "high school"
    UNDERGRADUATE = "undergraduate"
    MASTERS = "masters"
    PHD = "phd"

    EDUCATION_TYPE = (
        (NONE, "None"),
        (HIGH_SCHOOL, "high school"),
        (UNDERGRADUATE, "undergraduate"),
        (MASTERS, "masters"),
        (PHD, "phd"),)
        
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birthday = models.DateField(auto_now=False, auto_now_add=False)
    favorite_activies = models.TextField()
    email = models.EmailField(max_length=254)
    education = models.CharField(max_length=100, choices= EDUCATION_TYPE, default=NONE)


class Article(models.Model):
    title = models.CharField(max_length=100)
    published_date = models.DateField(auto_now=False, auto_now_add=False)
    content = models.TextField()
    writer = models.ForeignKey('Author', null=True, on_delete=models.SET_NULL)

    
