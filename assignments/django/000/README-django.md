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

3. 