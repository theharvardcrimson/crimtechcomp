from django.shortcuts import render
from django.http import HttpResponse
from my_app.models import *
# Create your views here

def index(request):
    return HttpResponse('Hello, world!')

def articles(request):
    articles_c = Article.objects.all()
    return render(request, "articles.html", context={"articles":articles_c})

def authors(request):
    authors_c = Author.objects.all()
    return render(request, "authors.html", context={"authors":authors_c})
