# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birthday = models.DateField()
    favorite_activities = models.TextField()
    email = models.EmailField()
    EDUCATION_CHOICES = (
        (NONE, 'none'),
        (HIGH SCHOOL, 'high school'),
        (UNDERGRADUATE, 'undergraduate'),
        (MASTERS, 'masters'),
        (PHD,'phd'),
    )
    education = models.CharField(choices=EDUCATION_CHOICES)


class Article(models.Model):
    title = models.CharField(max_length=150)
    published_date = models.DateField()
    content = models.TextField()
    writer = models.ForeignKey(Author, on_delete=models.CASCADE)
