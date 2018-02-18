from django.db import models
# Create your models here.

class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birthday = models.DateField(max_length=100)
    favorite_activities = models.TextField(max_length=100)
    email = models.EmailField(max_length=100)

    NONE = "NONE"
    HS = "HIGH SCHOOL"
    UNDERGRAD = "UNDERGRADUATE"
    MASTERS = "MASTERS"
    PHD = "PHD"

    EDUCATION_CHOICES = (
    (NONE,"None") ,
    (HS, "High School"),
    (UNDERGRAD, "Undergraduate"),
    (MASTERS, "Masters"),
    (PHD, "PhD") )

    education = models.CharField(max_length=100,
                            choices = EDUCATION_CHOICES, default= NONE)

class Article(models.Model):
    title = models.CharField(max_length=150)
    published_date = models.DateField(max_length=150)
    content = models.TextField(max_length=150)
    writer = models.ForeignKey('Author', null=True, on_delete = models.SET_NULL)
