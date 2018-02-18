from django.shortcuts import render
from my_app.models import *
# Create your views here.
#from django.http import HttpResponse


#def index(request):
    #return HttpResponse("Hello, World!")

def articles(request):
    article_request = Article.objects.all()
    return render(request, "articles.html", context={"articles": article_request})

def authors(request):
    author_request = Author.objects.all()
    return render(request, "authors.html", context={"authors": author_request})
