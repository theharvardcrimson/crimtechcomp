# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.shortcuts import render
from .models import Article, Author
import datetime

# Create your views here.
def index(request):
    return HttpResponse('Hello, world!')

def articles(request):
    # a = Article(title="title 3", content="Lorem ipsum dolor sit amet, consectetur adipisicing elit. Odit, cumque.")
    # a.save()
    articles = Article.objects.all()
    return render(request, "articles.html", context={"articles": articles})

def authors(request):
    # a = Author(first_name="first", last_name="last", birthday=datetime.datetime.now(), favorite_activities="sleeping", email="a@a.com", education="none")
    # a.save()
    authors = Author.objects.all()
    return render(request, "authors.html", context={"authors": authors})
