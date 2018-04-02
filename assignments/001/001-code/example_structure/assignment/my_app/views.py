from django.shortcuts import render
from django.template import *

from models import Author, Article

from django.http import HttpResponse

# Create your views here.
def base(request):
	return render(request, "base.html")

def authors(request):
	author_list = Author.objects.all()
	return render(request, "authors.html", context={'author_list':author_list})

def articles(request):
	article_list = Article.objects.all()
	return render(request, "articles.html", context={'article_list':article_list})
