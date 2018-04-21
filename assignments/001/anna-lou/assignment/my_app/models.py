# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
# https://docs.djangoproject.com/en/2.0/ref/models/fields/

class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birthday = models.DateField(auto_now=False, auto_now_add=False)
    favorite_activities = models.TextField()
    email = models.EmailField(max_length=100)
    EDUC_CHOICES = (
        ('none', 'none'),
        ('high school', 'high school'),
        ('undergraduate', 'undergraduate'),
        ('masters', 'masters'),
        ('phd', 'phd'),
    )
    education = models.CharField(max_length=100, choices=EDUC_CHOICES)

class Article(models.Model):
    title = models.CharField(max_length=150)
    published_date = models.DateField(auto_now=False, auto_now_add=True)
    content = models.TextField()
    writer = models.ForeignKey('Author', on_delete=models.PROTECT)
