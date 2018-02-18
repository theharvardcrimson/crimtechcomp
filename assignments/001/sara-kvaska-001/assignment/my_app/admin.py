from django.contrib import admin

# Register your models here.
from my_app.models import *
admin.site.register(Article)
admin.site.register(Author)
