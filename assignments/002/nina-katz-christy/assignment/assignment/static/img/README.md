## Modularity

It's a good practice to keep all of your static assets neat and organized, which we've started for you. If you decide to keep a local image on here, then be sure to stick it in this folder, and reference it in your html with something like this:
```html
<img blah blah src="{% static 'img/my_img_name.png|jpg|jpeg|etc' %}">
```