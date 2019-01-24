### Django!

Finally! We've arrived at Django! It's a framework in Python used for building websites, and it's super cool. It does all sorts of things for us and makes life really easy, but it's also super powerful, and we use it here at The Crimson for all of our web stuff.

There are many, many aspects to Django, but we will be focusing in on getting you acquainted with the environment and how to use it properly. Hopefully, it's not too overwhelming, but you will come out of this with a pretty good grip on what exactly makes Django tick. You'll notice that we hand you a lot of starter code, but in reality it's not all that much. That being said, you will be able to run some stuff right off the bat. 

Before we dive in, we're going to explain MVT to you (hopefully for the millionth time) because it's a useful design framework that you'll encounter all over the place. MVT stands for Models, Views, and Templates. It's a variant on MVC (Models, Views, Controllers) used by Django, and Django has conveniently separated out all of its parts to correspond nicely to this framework. Models are our data...kinda. We should say that you should strongly associated models with data. They deal with how data is represented, how you interact with your data, and how your data is stored. You can find Django models in any Django app's _models.py_ (crazy). Thus, to say that they _are_ your data is a bit of an understatement. Views in MVT are what happens when a client (or user or you) requests a given URL - should they receive a webpage, a JSON response, should data be processed? Views in Django are found in...you guessed it, _views.py_ files within apps. And finally, templates are Django's way of displaying things to the user. These roughly correspond to HTML, but we say roughly because 1) JavaScript, CSS, and other goodies are involved, and 2) Django has a built in templating engine that allows us to design templates for extensible use. For example, you can write a _base.html_ template for Django, then extend that in every other webpage for your website, abstracting out all the common bits to this _base.html_ (i.e. a navbar, footer, etc.). This makes for good programming practices, even in designing webpages. 

And, last bit of lecturing from us before you get started - Django is organized into projects and apps. When you begin, you start a project, which will include a main app by default. This main app always shares the same name as the project's name. Then, you can create new apps to satisfy new purposes, maybe you have a _web_ app and an _api_ app that handle your web and API requests, respectively. This helps make for a very clean, modular design that is easy to edit and maintain, as well as easy to collaborate on. 

Ok, let's get crackin'.

-----

### Assignment Spec

1. Ok, so you should have unzipped our supplied file and received a directory structure that looks like this:
```
myproject/
├── api
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── migrations
│   │   └── __init__.py
│   ├── models.py
│   ├── tests.py
│   └── views.py
├── manage.py
├── myproject
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── web
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── migrations
    │   └── __init__.py
    ├── models.py
    ├── tests.py
    └── views.py
```
This means that you have a project called _myproject_ with a main app called _myproject_ with two other apps called _api_ and _web_. If that sounds super unoriginal, then you're 100% correct because we're not known for our creativity. We created the project by first ```pip3 install django```, which gives us access to Django, then we ran the commands ```django-admin startproject myproject```, which created the project and main app, then we navigated into the _myproject/_ directory and ran ```django-admin startapp api``` and ```django-admin startapp web```, which created our other two apps. If you'd like to give this project a test run, then navigate into the directory containing _manage.py_ and run ```python3 manage.py runserver 0.0.0.0:8888```. This tells Django to run this webserver, exposing it to the world via the current computer on port 8888. If you'd like to see a rocketship, then you should navigate to your web browser of choice and go to ```127.0.0.1:8888``` or ```localhost:8888```. Localhost and 127.0.0.1 are roughly equivalent. Think about how google.com gets translated into some IP address 1.2.3.4 by DNS, and that should help you understand why the previous statement is true. Congrats, you have run a local webserver and accessed it!

2. Ok, now a lot of Django initially is getting acquainted with how to set everything up. Coincidentally, almost all of the initial important setup is done in a file called _settings.py_. There is only one, so you shouldn't have too much trouble locating it. Open it with you favorite text editor, and take a look inside. You should notice a bunch of Django-accessible constants that're in caps, like ALLOWED_HOSTS and INSTALLED_APPS. You may be asking how you know that they're Django-accessible, and the answer is...you only know because we told you, don't worry! We are going to need to make some important modifications, namely in those two constants we mentioned. ALLOWED_HOSTS tells this Django project which hosts or computers it's allowed to run on. Just to be sure, let's add '127.0.0.1' and 'localhost' (with the quotes! this constant is a list of Python strings representing hosts). This allows Django for sure to run on our local machine. If we were to deploy this webserver to an actual website under the domain name 'mydomain.io' then we would want to make sure to add 'mydomain.io' to this constant. Next, let's add to the INSTALLED_APPS constant, at the bottom. Order matters for INSTALLED_APPS, so make sure to put our new apps at the bottom and make sure that the main app is the first of the 3. This helps us understand where naming problems may arise later. We should add 'myproject', 'api', and 'web', since these are our new apps. This also tells Django to check for a _templates/_ directory within each of these apps when it's looking for templates. In fact, let's go ahead and create _templates/_ directories inside each of our apps. The one inside the main app, _myproject_ should contain universal templates, like _base.html_, and then the other _templates/_ directories inside of _web_ and _api_ should contain only templates relevant to those apps. This helps us stay organized. 

3. We're now going to acquaint ourselves with how new requests to Django are routed through the application. When a user visits our site, for example, they're at the default URL path of ```/```, which is just the base path on our host ("mydomain.io", for example). This initial request is a GET request by default (our user wants to "get" information from us), and Django knows that it is asking for whatever mechanism we have placed behind the ```/``` URL or route. The way it knows this though is through _urls.py_. This file tells Django how to map between requested URLs, routes, or paths, and the mechanisms and controls we have in our application. We can also tell Django to go check a different set of URLs if a certain pattern is matched. For example, if we want all ```/``` requests to go to _web_ and be handled by _web_'s _urls.py_ then we can put this code into _myproject_'s _urls.py_: ```import web.urls as web_urls```. Now we have access to all of _web_'s URLs in _myproject_'s _urls.py_. What this means for us is that we can have all URLs that aren't matched by other patterns get sent off to the _web_ app to be handled. In order to do this, we're going to add _re\_path_ and _include_ to the things we import from _django.urls_. _re\_path_ stands for "regular expressions path", which means we can match URLs using regular expressions. The one we're going to use it pretty easy though: ```path('', include(web_urls))```. This code says anything that gets here will be sent to _web_'s _urls.py_ for further matching. In essence, we've said that our default option is to have the _web_ app handle requests. 

4. This brings us to the next task, which is to add a _urls.py_ to the _web/_ directory/app. We will do this manually, and then we'll add the essential line of code: ```from django.urls import path```, which allows us to do that matching that we discussed above. We'll get started with a very simple one. Let's just match the blank path (```/```) to a standard view: ```index```. This code would look like ```path('', index)```. But where did _index_ come from? What is it? It should be a view, defined in some _views.py_. So we're going to import that view at the top of our file. Let's do that by saying ```from web.views import *```. Now, let's go create that view. 

5. Within _web_'s _views.py_, we will define each of our views, which are really just Python functions. In their simplest form, they take in as a parameter a request object, and they return some form of Response object (frequently, an HTTPResponse object, though JSON Responses are also valid). For example, our first view might look like this: 
```
def index(request):
    return render(request, 'index.html')
```
This allows us to return our index page by default. 

6. Now, we need to go create that index page (see how each thing is kinda motivated in this long chain? this is _a_ style of design, though not the best one in all cases, it is rather convenient for learning). Anyways, let's create that _index.html_ file in _web/templates/_. We're going to use a mix of HTML and templating language, which is usually denoted by statements that are wrapped in either ```{{ }}``` or ```{% %}```, with the former indicating values and the latter indicating functions. Often, Django's templating language looks a lot like Python, so you should be somewhat familiar with the syntax. In fact, here's some mock code for our index page: 
```
{% extends 'base.html' %}

{% block title %}
    Home
{% endblock %}

{% block body %}
    {% if 2 > 3 %}
        <h1>Yodku, akeld!</h1>
    {% else %}
        <h1>Hello, world!</h1>
    {% endif %}
{% endblock %}
```
Take a guess as to what that does! It's pretty cool as a concept - code that allows us to manipulate something static before it gets handed to the client/user. Think about how this is different from JavaScript!

7. Lastly, we need to create the file that our _index.html_ extends - _base.html_. This is the overall template that should be used to create all pages on our website. Since it's a universal file, we're going to put it into the main app's templates - _myproject/templates/_. In this file, we'll set up the sections or blocks that we expect to be used by the children of this file (like _index.html_) and we'll add some universal traits, like the metadata that goes at the top of the page. Please refer to the HTML assignment in order to see what kinds of metadata might go here. This file should most resemble the standard HTML document, but the below is an example stripped of many of its specifics:
```
<!DOCTYPE html>
    <head>
        <title>{% block title %}{% endblock %}</title>
    </head>

    <body>
        {% block body %}
        {% endblock %}
    </body>
</html>
```
Can you see how this document would be great as a template for _index.html_ to extend? Play around with adding your own tweaks in order to understand better how it works. 

8. In this assignment, we're not going to touch much else in terms of implementing the rest of the webserver, with models and things. However, we will ask you to create a bunch of new HTML pages. The next assignment will have you link those pages to things in the backend (the Python). Feel free to use Bootstrap if you'd like to make your life a little bit easier. Within the _web_ app, please create a new set of HTML documents that all extend the 'base.html' document. There should be a _submit.html_, a _results.html_, and a _dashboard.html_. _submit.html_ should have a form that allows a user to submit named inputs: first_name, last_name, height, weight, age, and blood type. Height, weight, and age should all be numeric inputs. The names should be standard text inputs. The blood type should be a select input. _results.html_ should display the some stats about the person, probably in some form of table that shows how those stats are calculated. The important stat will be the person's BMI. Note that in order to pass information from a view to a Django template we can use syntax like the following: 
```
# in views.py
myvar = 42
context = {'varname': myvar}
return render(request, 'blah.html', context=context)

# in blah.html
<h1>{{ varname }}</h1>
```
Thus, in _blah.html_, we will see the number 42 displayed in h1-size font and styling. Hopefully this makes sense, though we know that it can take a while to become used to. Finally, _dashboard.html_ should allow a user to select which webpage they'd like to navigate to, picking from a list of previous results or choosing to submit a new set of information. It doesn't matter much how this is implemented, since this is mostly just HTML for navigation. 

9. If you would like, please add a navbar to _base.html_ so that your website is easier to navigate. 

10. Go ahead and submit - this should feel incomplete, and that's ok, we're just having you set everything up, and then we'll tie it together in the next assignment. 