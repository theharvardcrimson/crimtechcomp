## 003

------

### Logistics

The first part of this assignment is just getting the urls working properly - do you have three views, three urls, and three webpages? It is due as assignment 003

The second part is adding onto the first part; have you implemented the two functions that are asked of you (they'll be in their respective views.py files)? This is due as assignment 004

The third and final part is building the local version of the assignment, where a user can somehow select a local option, and have their encryption happen live, without needing to send it to the Django server. In essence, implement the two functions from part 2 in JS. This is assignment 005

------

Heylo E'rybody!

So we're back at it again with that Django, and we ask that you build your own app from scratch again, because \*yes\*, that is something that is kinda just generally useful to remember how to do. You shouldn't execute these steps yet, but just keep them in mind as you read the assignment!

  1. Check your surroundings, are you in the right kind of environment (Django 1.8, which you can check with ```django-admin --version```) - i.e. virtualenv?

  2. Do you remember the ```django-admin``` command to start a project? How about to start an app within that project?

  3. Once you have a project "my_project", did you remember to copy "urls.py" from "my_project/my_project/urls.py" to "my_project/my_app/urls.py" (you also need to include the latter "urls.py" in the former, do you remember how?)

  4. Have you installed "my_app" in "settings.py"? Do you remember how?

  5. How about allowed "localhost" and "127.0.0.1" in the same file?

  6. Finally, have you created a "static/" directory in "my_project/my_project/" and a "templates/" directory in "my_project/my_app"?

With all of that in mind, do you know where your ".html" documents go? How about your ".css/.js/.img" ones?

I know it's a lot to remember, but I promise that as you do this more, the flow starts to make more sense and becomes just a part of the way you look at this.

Sorry to make you read more, but one last little mental exercise, can you describe the flow of an HTTP request to your Django site/server?

  1. Client sends the HTTP request, r (POST/GET usually)
  2. Django server receives the request and looks for a URL that matches the one in the request (we could imagine this like r.url) in the main project's "urls.py" ("my_project/my_project/urls.py")
  3. Upon finding a matching URL, Django goes to the view specified by that URL in "urls.py" (where's that view located?)
  4. In the appropriate view in "views.py", the view is passed r, our request (remember, views are functions that take in a request and return some form of HTTPResponse or rendered HTML document)
  5. The view then processes our request, and returns some form of response to the Django server, which then serves up that response to the user

Now let's get coding!

------

### Assignment 003

Your mission, Double-O Forty-Two, should you choose to accept (sorry it's not much of a choice in this case, but hey, spy movie references!), is to complete the following tasks. If you've ever played a capture-the-flag (CTF), then you may recognize this style of game! (Tip: I would advise decoding each step first, then attempting the assignment!)

Remember your training (which included extensive talks on cryptography, especially things like binary encoding, ASCII encoding, Caesar ciphers, hexadecimal encoding, and base64 encoding)!

Structure:
```
crypto
├── challenge.txt
├── crypto
│   ├── __init__.py
│   ├── settings.py
│   ├── templates
│   │   ├── base.html
│   │   └── result.html
│   ├── urls.py
│   ├── views.py
│   └── wsgi.py
├── db.sqlite3
├── decode
│   ├── __init__.py
│   ├── admin.py
│   ├── migrations
│   │   ├── __init__.py
│   │   └── __init__.pyc
│   ├── models.py
│   ├── templates
│   │   └── decode.html
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── encode
│   ├── __init__.py
│   ├── admin.py
│   ├── migrations
│   │   ├── __init__.py
│   │   └── __init__.pyc
│   ├── models.py
│   ├── templates
│   │   └── encode.html
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── flags.txt
└── manage.py
```

0. If you want an example of this project, go ahead and visit crimtechcomp-crypto.herokuapp.com for an example! (Don't worry, all of the code is somewhat obfuscated, it won't ruin your fun :D). Play around with visiting varying urls on the site to see how it should work, but in general, we want visiting "127.0.0.1:8000/encode/____" to display a webpage with two text boxes. The first should be small, for a key (string used to encrypt our message), and the second to receive the message to be encrypted. Upon submitting, the user should receive the encrypted message. Correspondingly, we want "127.0.0.1:8000/decode/____" to have two text inputs, one for a key, and one for the encoded message. Upon submission, this should return the decoded message. We ask that you implement a Vigenere's cypher (with a twist!) later on, and tell you how to do so!


1. First, decode this task. The flag is - thisismyfirstflag - Now you may wonder, "what do I do with this flag?" The answer is to paste it (and all other flags, one per line) in a file "flags.txt" in the same directory as your "manage.py" (which you don't have yet, so you better start a Django project called "crypto", don't include the - " -!)

2. Your next task is to create two apps in your crypto project. They should be called "encode" and "decode". Your next flag is "udshofjtushofj"

3. Wonderful! That's three kinds of encoding - binary, caesar cypher, and JSFuck!

4. I know, we're annoying! But hopefully also at least mildly entertaining? We've detailed the rest of this task below, and though it seems like a lot, don't worry, we'll make sure to provide you with lots of information...encrypted of course!

5. So you have two apps (did you remember to install them properly and everything?). The urls that point to your respective apps should be like this: url(r'^encode/.*', encode_urls) and something similar for decode. These urls go in the "crypto/crypto/urls.py". This instruction's flag is "hexy646563696D616C". In each app's "urls.py" (remember you have to create your own!), there should only be one url, the general one of the form: url(r'^.*', encode_view) (or decode_view for the other app!)

6. Cool! So now, let's talk about how we'll build the actual logic of the project. There should be two functions, in their respective apps' "views.py" which perform server-side or Python code to accomplish your given tasks. These functions should be separate from the views themselves, so that we can test that they work properly without using your views. If you're wondering what that might look like, here's an example:

In "views.py":
```python
def calculate(x, y, f): #<-- this is just a function
  f = f.strip().lower()
  if f == 'add':
    return x + y
  elif f == 'subtract':
    return x - y
  elif f == 'multiply':
    return x * y
  elif f == 'divide':
    return x / y
  elif f == 'power':
    return x ** y
  else
    return None

def my_view_name(request): #<-- this is a view
  if request.method == 'POST':
    context = {'calculation': None}

    x, y = request.POST['x'], request.POST['y']
    fun = request.POST['function']

    context['calculation'] = calculate(x, y, fun)

    return render(request, 'calculated.html', context=context)

  else:
    return render(request, 'my_page_name.html')
```
Can you see how the above would work? How about in the context of this assignment? This is a separation of logic that lets us debug the two main ideas separately: the request-handling logic, and the actual math logic. Back to annoying "ciphers"!

7. We ask that you call your functions "encode" and "decode", and your views "encode_view" and "decode_view", respectively. Your functions should each take in two strings, and output one string (why strings?). And they should do the actual encrypting heavy lifting. Your views should be fairly simple, similar to the example above, where they make a call to either encode or decode, and then render an HTML template with the result as context. Now, the behavior of encrypt(msg, k) is like this: given a message, msg, and a key, k, the function should iterate through the string and add the value of the key's letter to the value of the message's letter in the corresponding position. This is a cipher known as Vigenere's Cipher. However, we've added a twist! We ask that when you get to the end of the key, you go backwards through the key, bouncing back and forth until the entire message is encrypted. Always start by going through the key forward! This means that encode('aaaaaaaaaa', 'abc') -> 'bcddcbbcdd'. Also, numbers should be left untouched, but should still move your position in the key, so encode('12a', 'abc') -> '12d'. And of course given some key and msg, decode(encode(msg, key), key) -> msg. There are test cases for check, which should help. Just make sure to separate the encode and decode functions from the views that use them!

9. Awesome! Now you've done all of the backend stuff, so you might be wondering "how TF do I build the frontend for this?" We ask that you do not literally copy the HTML from our example site, but rather attempt it on your own, with some pointers from us. In fact, why don't you go look [here](https://v4-alpha.getbootstrap.com/getting-started/introduction/#quick-start "Bootstrap Quickstart"). And see if that helps you get started building some HTML. Specifically, you'll want to build an HTML form with two fields and a way to submit the form (for forms with Django, you need to include the tag ```{% csrf_token %}```). Your form might look something like this:
```html
<form method="post">
    <input name="thing1" placeholder="I'm thing1"/>
    <input name="thing2" placeholder="I'm thing2"/>
    <button type="submit">Submit Me!</button>
    {% csrf_token %}
</form>
```
Then, in "views.py", you might handle those items like this:
```python
if 'thing1' in request.POST and 'thing2' in request.POST:
  result = calculate(41, 1, 'add')
  context = {
    'user_input': request.POST['thing1'],
    'user_input2': request.POST['thing2'],
    'result': result
  }
return render(request, 'my_template.html', context=context)
```

And lastly, "my_template.html" might look like this:
```html
{% extends 'base.html' %}

{% block body %}
  <p>{{ user_input }} was your first input</p>
  <p>{{ user_input2 }} was your second input</p>
  <h3>The result was {{ result }}</h3>
{% endblock %}
```

10. So you're ready to build this fancy dandy webapp, with a couple of urls, at least 3 webpages, and some cool applications. Now, for the kinda annoying part: we ask that you take some time to debug this at every single step. We've written checks for you to make debugging a bit easier, but there will be annoying things. We've also outlined the structure above (way up there!), and we ask that you keep names the same in order for checks to pass correctly! We also ask that you use a "base.html" for all webpage attributes that are common to each webpage (it should be in the crypto app's "templates/" directory, and make sure the app is in INSTALLED_APPS!) Once you're comfortable with all of this, you'll have almost finished your mission! Your last two tasks are below!

11. \*\*This is a big task, but easy if you've completed the Python one!\*\* Please allow for a "local" option on your webpage (how could you do the Python function above in Javascript?) and when it is selected, perform the tasks above locally (do not submit a request to the Django server), so that your user can get their output without refreshing/changing pages (maybe even live?).

12. You're almost done! Finally, include a file in the same directory as your "manage.py" called "challenge.txt" which contains a single word, on its own line. This word should have been encrypted any way you see fit (that can still be decrypted), and it should be a word you'd recognize if you saw it somewhere. This challenge is not for you, but rather us - can you encrypt it so well that your beloved comp directors cannot figure out the word?

Best of luck, agent! We believe in you, and we know this assignment is long (but you have 3 weeks to do it, with chunks due at 1 week intervals). Come to OH, ask us questions, and in general don't be afraid to get help! Please don't spend any more than 6-8 hours total on this assignment (over the course of three weeks!)

<3,

Nick \&\& Richard
