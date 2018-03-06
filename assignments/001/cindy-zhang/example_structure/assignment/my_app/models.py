from django.db import models

# Create your models here.
class Author(models.Model):

  EDUCATION_CHOICES = (
    ('no', 'None'),
    ('hs', 'High School'),
    ('ug', 'Undergraduate'),
    ('ma', 'Masters'),
    ('ph', 'PhD'),
  )

  first_name = models.CharField(max_length=100)
  last_name = models.CharField(max_length=150)
  birthday = models.DateField(auto_now=False, auto_now_add=False)
  favorite_activities = models.TextField()
  email = models.EmailField()
  education = models.CharField(choices=EDUCATION_CHOICES)

class Article(models.Model):
  title=models.CharField(max_length=150)
  published_date = models.DateField(auto_now=False, auto_now_add=False)
  content = models.TextField()
  writer = models.ForeignKey('Author', null=True, on_delete=models.SET_NULL)


  
