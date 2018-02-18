from django.http import HttpResponse
from django.shortcuts import render
from my_app.models import *

# Create your views here.
def index(request):
    return HttpResponse('Hello, world!')

def articles(request):
	return render(request, "articles.html", context={"articles": [{"title" : "Title1", "content" : "Content1"}, {"title" : "Title2", "content" : "Content2"}]})

def authors(request):
	return render(request, "authors.html", context={"authors": [{"first_name" : "Foo", "last_name" : "Bar"}, {"first_name" : "Boo", "last_name" : "Far"}]})