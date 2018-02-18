from django.shortcuts import render
from django.http import HttpResponse

from .models import Author, Article

def index(request):
    article_list = Article.objects.filter()
    return render(request, "articles.html", context={"articles": article_list})

def authors(request):
    author_list = Author.objects.filter()
    return render(request, "authors.html", context={"authors": author_list})
