# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birthday = models.DateField(auto_now=False, auto_now_add=False)
    favorite_activites = models.TextField()
    email = models.EmailField(max_length=254)
    EDUCATION_CHOICES = ["none", "high school", "undergraduate", "masters", "phd"]
    education = models.CharField(max_length=100, choices=EDUCATION_CHOICES, default="none")

class Article(models.Model):
    title = models.CharField(max_length=150)
    published_date = models.DateField(auto_now=False, auto_now_add=False)
    content = models.TextField()
    writer = models.ForeignKey(Author, on_delete=models.PROTECT)
