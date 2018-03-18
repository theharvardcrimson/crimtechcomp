from django.shortcuts import render
from django.http import HttpResponse
from my_app.models import Article, Author

# Create your views here.
def index(request):
 return HttpResponse('Hello,world!')

def articles(request):
  a = Article.objects.all()
  return render(request, "articles.html", context={"articles":a})

def author(request):
  a = Author.objects.all()
  return render(request, "authors.html", context={"authors":a})


