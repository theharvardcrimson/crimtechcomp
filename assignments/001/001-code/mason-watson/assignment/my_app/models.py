from django.db import models

# Create your models here.
class Author(models.Model):
    NONE = "NONE"
    HIGH_SCHOOL = "HIGH SCHOOL"
    UNDERGRADUATE = "UNDERGRADUATE"
    MASTERS = "MASTERS"
    PHD = "PHD"

    EDUCATION_CHOICES = (
       (NONE, "None"),
       (HIGH_SCHOOL, "High School"),
       (UNDERGRADUATE, "Undergraduate"),
       (MASTERS, "Masters"),
       (PHD, "PhD")
    )

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birthday = models.DateField()
    favorite_activities = models.TextField()
    email = models.EmailField()
    education = models.CharField(max_length=25, choices=EDUCATION_CHOICES, default=NONE)

class Article(models.Model):
    title = models.CharField(max_length=150)
    published_date = models.DateField()
    content = models.TextField()
    writer = models.ForeignKey('Author', null=True, on_delete=models.SET_NULL)
