## 001

------

Hey Y'all!

So we've included a requirements.txt file in this directory. Please double check that you're working within the virtual environment you've decided to use for this comp (do you remember how?) and then run
```bash
pip install -r requirements.txt
```
and this will install the appropriate requirements. Requirements.txt files are super useful for almost any Python project!

------

Now on to the important part! DJANGO!!!! It's a pretty neat framework (written in Python of course) for building webpages. In fact, thecrimson.com is built on Django. And we're going to get you going with it too! In the meeting, we helped you build a simple website, and here we will ask that you basically do just that, although you'll have what we gave you to build on. In the example_structure directory, we've included the structure that should basically be followed, except we haven't filled anything in, and there are some missing files!
```
assignment/
├── assignment
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── manage.py
└── my_app
    ├── __init__.py
    ├── admin.py
    ├── migrations
    │   └── __init__.py
    ├── models.py
    ├── tests.py
    └── views.py
```
When you run ```django-admin startproject assignment```, it should be run in the "your-name/" directory. And for running ```check 001```, you should be within the root of your Django project, or in "your-name/assignment/"

-----

Assignment!

Please read through all of the following before beginning the assignment, particularly the last point!

Also, note that while ```check 001``` can be used for anything python here, it will not be able to help you with your HTML, so be aware that even once all of your checks pass, you still may have some work to do! We're working hard to automate HTML testing too, but we also want to improve the experience of working with ```check``` in general!

Alright, and here's the assignment for this week:

1. So in the meeting, we got you acquainted with the django-admin commands ```startproject``` and ```startapp```. We expect that you will have a project with the title "assignment" with an app called "my_app". We technically aren't checking for any other apps, so if you have apps named other things, it won't matter to us. 

2. Now, you might be wondering, "how do I use this django thing?" And to see it in action, go ahead and find the directory with "manage.py" in it (should be the main "assignment/" directory). From there, you can run ```python manage.py runserver 0.0.0.0:8000``` which tells Django to run locally and bind to port 8000. If you want to view your site, go ahead and head over to "127.0.0.1:8000" or "localhost:8000" in your web browser of choice. Note, the text in red about unapplied migrations has to do with your models and database - you can fix it by running ```python manage.py makemigrations``` and then ```python manage.py migrate```

3. On that webpage, you'll see a cute little message from Django and not much else. So now it's time for you to start building! If you haven't already please run ```django-admin startapp my_app``` in the same directory as "manage.py". This will create a lot of the files you'll need to have a fully-functioning basic web application. You should now have a folder called "my_app" in the "assignment/" directory. 

4. Now, we have to "wire" it all up! This is where our discussion on MVT (not "movement"!) becomes a bit more relevant! Django uses URL pattern-matching to take a request it receives, and deliver it to the appropriate _view_ in your app. So first, let's set up a simple view so that those GET requests have somewhere to go. In "my_app/views.py" add the line "from django.http import HttpResponse" at the top. And define a view as follows:
```python
def index(request):
    return HttpResponse('Hello, world!')
```
This view is called "index" and takes in some request, which is the representation of the request your django server received, then it returns an HttpResponse with the text 'Hello, world!'

5. Now, we need to tell django when to pass a request into this view. In "my_app/" you should create a file called "urls.py" and inside, we're going to build the pattern that lets django know where to tango. 
```python
from django.conf.urls import url
from my_app.views import *

urlpatterns = [
    url(r'^', index, name='index'),
]
```
This imports all of our views from "my\_app/views.py" (note that in python, we import as if those are modules, with "my\_app.views"). The "urlpatterns" object contains all urls which django will use to pattern-match for your app, and in this case we're using the open pattern "^" which will match anything that has a beginning, and telling it to direct a request that matches that pattern to the "index" view, which we've named "index". You may ask "where does this url come from?" The answer is: your web browser! What you type in, such as "localhost:8000/my\_cool\_homepage" will come through to Django as "my\_cool\_homepage", which would match with "^" in this case, and get passed along to our "index" view. 

6. We're not done quite yet though, because we still need to go to the main "urls.py" file and add a pattern. Go ahead an open up "assignment/assignment/urls.py" and adjust it to look like the following:
```python
from django.conf.urls import include, url
from django.contrib import admin

from my_app import urls as my_app_urls

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include(my_app_urls)),
]
```
Note the importing of "include" and the order of the pattern matching (the source of many a bug!). This is a slightly different kind of use for "urlpatterns". Instead of matching a url and sending the request to a specific view, we're matching the url and then telling Django to go and match it against another suite of url pattern-matches (specifically, the one we just set up a few minutes ago). 

7. Now it seems like we should be good to go! Let's go back to "assignment/" and run the "manage.py" runserver command (```python manage.py runserver 0.0.0.0:8000```).

8. While it wasn't a problem here, you should be aware of the "ALLOWED\_HOSTS" variable in Django settings. It tells Django which hosts (domain names, IP addresses) it's allowed to be run on. It won't hurt you to add these two hosts to the "ALLOWED\_HOSTS" list, but we do not require it. 
```
ALLOWED_HOSTS = ['127.0.0.1', 'localhost']
```
Please go ahead and look up "localhost" and "127.0.0.1", and using the knowledge that "ALLOWED_HOSTS" tells Django what IP/Domains are ok to run on, explain to yourself why we included those two. 

9. Now that you have a basic Djan*go* *flow* *go*ing, let's touch on the other parts of MVT (we've only done "V"). "M," as you know, stands for "Models" and if you go into "my_app/models.py" you can see...absolutely nothing! This is the first tricky part of this assignment - we want you to make two of your own models. There's already a built-in model for Django, the User model, but we also want Author and Article models. To get you started, we'll tell you that they'll have at least these attributes:
```python
from django.db import models

# Create your models here.
class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    ...more stuff goes here

class Article(models.Model):
    title = models.CharField(max_length=150)
    ...more stuff here too!
```

10. For this next part, you may want to reference what "fields" exist in django and how to use them (plus, being able to read documentation is a great skill): https://docs.djangoproject.com/en/2.0/ref/models/fields/ 

11. Now, we ask that the Author model have the following fields: first\_name, last\_name, birthday, favorite\_activities, email, and education. The birthday should be a DateField, favorite\_activities should be a TextField, email should be an EmailField, and Education should be a CharField. Additionally, we ask that education be a set of choices from "none", "high school", "undergraduate", "masters", and "phd". (Try googling "Django charfield choices")

12. Finally, the Article model should have the following fields: title, published\_date, content, and writer. The published\_date should be a DateField, content should be a TextField, and writer should be a ForiegnKey (do some googling!). Something to note about that last bit (the ForeignKey) is should articles disappear if their author is removed? Or should they stay around? This has to do with the on_delete option passed in to the ForeignKey field. 

13. The final section of this assignment is to create two views (feel free to use the index view as one of them): one for displaying the articles, and one for displaying the authors. When the view for the articles is reached, it should return a webpage displaying all the "articles" in a column, and when the view for authors is reached, it should return a webpage displaying all the "authors" in a column. Yes, this is very contrived/simple, but what is a blog website but a list of articles and authors?

14. To achieve this, we will need to go into templates - how do we build webpages dynamically? In your "my\_app/" directory, please add another folder called "templates". Then, in "my\_app/templates/" add three files: "base.html", "articles.html", and "authors.html". These will be the html files that you will use to get everything to look pretty!

15. In django, templating makes generating consistent and beautiful HTML very easy - we will put all of our standard content that we want on every page in "base.html" (think navbars, headers, and footers). And then adjust the main content and title within each page. Your "base.html" might look like this:
```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

    <title>
        {% block title %}{% endblock %}
    </title>
  </head>
  <body>
    <!-- navbar here! -->
    
    {% block body %}
    {% endblock %}

  </body>
</html>
```

Then, in order to build any of our content pages, we can simply do this:
```html
{% block title %}
My Webpage Title Goes Here
{% endblock %}

{% block body %}
MY CONTENT GOES HERE
{% endblock %}
``` 
Generally, this makes life easier, but it also makes life more consistent, which is also usually a good thing. See those curly braces with the percent-signs? That is part of the magic of Django templating - those tell Django to do some extra stuff right before the webpage gets returned to the user. In this case, you're only seeing the ones for blocks, which are literally like "replacement" commands, where all of the content in a content page between the {% block %} and {% endblock %} tags gets shoved into the corresponding tags in "base.html" when the page gets built. Another tag you might find useful behaves like this:
```html
{% for article in articles %}
<div>
    <h2>{{ article.title }}</h2>
    <p>{{ article.content }}</p>
</div>
{% endfor %}
```
In order for this to work, the template has to be rendered with a "context" or with knowledge of what the "articles" variable is. This means that in your view that renders this template, it should return not an HttpResponse object, but rather something like this:
```python
return render(request, "articles.html", context={"articles": ???})
```
More generally, if your view returns this:
```python
bar = [6, 7]
return render(request, "foo.html", context={"foo": bar, "baz": 42})
```
Then in "foo.html", you can write:
```html
{% block body %}
<div>
    <h1>{{ baz }}</h1>
    <p>{% for i in foo %}{{ i }}{% endfor %}</p>
</div>
``` 
Any guesses as to what this HTML page would look like? Can you see which tag I forgot to include?

16. Whew, I know that this is a really long document with a ton of reading, but if you complete the enormous tasks outlined above, you will have a pretty solid foundation in Django, with the ability to build some pretty crazy things. We know this is a lot to take in, and that you'll have lots of questions - so please email us, please come to our office hours, and please don't spend too long working on this!

Best,


Your Comp Directors