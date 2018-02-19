from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse('Hello, world!')
# Create your views here.

def author(request):
	return render(request, "authors.html", context = {"authors": request})

def article(request):
	return render(request, "articles.html", context = {"articles": request})
