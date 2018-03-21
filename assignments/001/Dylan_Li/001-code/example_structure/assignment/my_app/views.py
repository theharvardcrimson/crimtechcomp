from django.shortcuts import render
from django.http import HttpResponse
from models import Article, Author
import datetime

# Create your views here.
def index(request):
	return HttpResponse('Hello, world')

def authors(request):
	# return HttpResponse('Hello, world!!!!')
	# a = Author(first_name="dylan", last_name="li", birthday=datetime.datetime.now(), favorite_activities="eating", email="dylanlix@gmail", education="high school")
	# a.save()
	authors = Author.objects.all()
	return render(request, 'authors.html', context={'authors': authors})

def articles(request):
	# return HttpResponse('Hello, world!!!!')
	# a = Author(first_name="dylan", last_name="li", birthday=datetime.datetime.now(), favorite_activities="eating", email="dylanlix@gmail", education="high school")
	# a.save()
	authors = Articles.objects.all()
	return render(request, 'authors.html', context={'authors': authors})