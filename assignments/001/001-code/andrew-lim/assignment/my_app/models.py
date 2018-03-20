from django.db import models
from datetime import date
from django.core.exceptions import ValidationError

# Create your models here.
class Author(models.Model):
    NONE = 'NO'
    HIGH_SCHOOL = 'HS'
    UNDERGRADUATE = 'UG'
    MASTERS = 'MS'
    PHD = 'PH'
    EDUCATION_CHOICES = (
        (NONE, 'None'),
        (HIGH_SCHOOL, 'High School'),
        (UNDERGRADUATE, 'Undergraduate'),
        (MASTERS, 'Masters'),
        (PHD, 'PHD'),
    )

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birthday = models.DateField()
    favorite_activities = models.TextField()
    email = models.EmailField()
    education = models.CharField(max_length=2, choices=EDUCATION_CHOICES)

class Article(models.Model):
    title = models.CharField(max_length=150)
    published_date = models.DateField()
    content = models.TextField()
    writer = models.ForeignKey('Author', on_delete=models.PROTECT)
