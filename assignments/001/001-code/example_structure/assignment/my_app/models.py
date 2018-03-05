from django.db import models

# Create your models here.
class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birthday = models.DateField(auto_now=False, auto_now_add=False)
    favorite_activities = models.TextField()
    email = models.EmailField(max_length=254)

    EDUCATION_LEVEL = (
    	('N/A', 'None'),
        ('HS', 'High School'),
        ('COL', 'College'),
        ('MA', 'Masters'),
        ('PHD', 'PhD'),
    )

    education = models.CharField(max_length=3, choices=EDUCATION_LEVEL)

    def __str__(self):
    	return self.first_name + " " + self.last_name 

class Article(models.Model):
    title = models.CharField(max_length=150)
    published_date = models.DateField(auto_now=False, auto_now_add=False)
    content = models.TextField()
    writer = models.ForeignKey(Author, on_delete=models.CASCADE)