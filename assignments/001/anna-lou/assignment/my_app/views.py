# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.shortcuts import render
from .models import Article, Author
import datetime

# Create your views here.
def index(request):
    return HttpResponse('Hello, world!<br>'
                        '<a href="/articles">Articles</a><br>'
                        '<a href="/authors">Authors</a>')

def articles(request):
    articles = Article.objects.all()
    return render(request, "articles.html", context={"articles": articles})

def authors(request):
    authors = Author.objects.all()
    return render(request, "authors.html", context={"authors": authors})
