# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birthday = models.DateField(auto_now=False, auto_now_add=False)
    favorite_activities = models.TextField()
    email = models.EmailField(max_length=254)
    education = models.CharField(max_length=100, choices=((NONE, 'None'), (HIGH_SCHOOL, 'High School'), (UNDERGRADUATE, 'Undergraduate'), (MASTERS, 'Masters'), (PHD, 'PHD')))

class Article(models.Model):
    title = models.CharField(max_length=150)
    published_date = models.DateField(auto_now=False, auto_now_add=False)
    content = models.TextField()
    writer = models.ForeignKey(Writer, on_delete=models.CASCADE)
    