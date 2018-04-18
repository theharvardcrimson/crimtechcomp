# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return HttpResponse('Hello, world!')

def articles(request):
    return render(request, "articles.html", context={"articles": {}})

def authors(request):
    return render(request, "authors.html", context={"authors": {}})
