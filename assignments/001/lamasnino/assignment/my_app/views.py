### fix article thing

from django.http import HttpResponse

from django.shortcuts import render

#from django.db import models

#from models import Author(models.Model),Article(models.Model)
from my_app.models import Article,Author

#from .models import Article,Author
# ^ ?

def index(request):
    return HttpResponse('H')

def articleView(request):
 #   article_list = [Article(title=('article1'),published_date=(),content=("words"),writer=('Anna Apple')),Article(title=('article2'),published_date=(),content=("more words"),writer=('Barb Beet'))]
    #article1=Article('title1','2006-10-25','words','writer1')
    #article2=Article('title2','10/25/2006','words','writer2')
    #article_list = [article1,article2]
    # article1='word'
    # article2='word2'
    
    #article_list=[article1,article2]
    #title1='title1'
    #published_date1='10.10.10'
    #content1='content1'
    #writer1='writer1'
    #education1='none'
    #article1=Article(title1,published_date1,content1,writer1)
    #title2='title2'
    #published_date2='1.10.10'
    #content2='content2'
    #writer2='writer2'
    #education2='none'
    #Author1=Author("Anna","Apple",'10.11.1813',"acting","anna@gmail.com","none")
    #Author2=Author("Barb","Beet",'10.11.1813',"acting","anna@gmail.com","none")
    article1=Article('',"title1","2.08.9120","content1","Anna Apple")
    article2=Article('',"title2","1.0.10","content2","Barb Beet")
    #article1=Article(title=('title1'),published_date=('10.10.10'),content=("content1"),writer=('writer 1'),education1=('none'))
    #article2=Article(title=('title2'),published_date=('1.10.11'),content=('content2'),writer=('writer2'),education2=('none'))
    article_list=[article1,article2]
    return render(request, "articles.html", context={"articles": article_list})
    #return render(request, "articles.html", context={"articles": Article(title='article1',published_date=(),content=("words"),writer=("Anna"),Article(title='article2',published_date=(),content=("more words"),writer=("Barb")})


def authorView(request):
    author_list=[Author(first_name=("Anna"),last_name=("Apple"),birthday=('10.11.1813'),favorite_activities=("acting"),email=("anna@gmail.com"),education=("none")),Author(first_name=("Barb"),last_name=("Beet"),birthday=('08.21.2007'),favorite_activities=("boating"),email=("barb@gmail.com"),education=("none"))]                         
    return render(request, "authors.html",context={"authors": author_list})
    pass 
    # return webpage displaying all authors in a column
    # return HttpResponse(i also dk)

    

# Create your views here.

