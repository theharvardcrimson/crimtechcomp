from django.db import models

# Create your models here.
import datetime

class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birthday = models.DateField(default=datetime.date.today())
    # or DateField)auto_now=False,auto_now_add=False)
    favorite_activities = models.TextField(max_length=100)
    # or favorite_activities = models.TextField()
    email = models.EmailField(max_length=100)
    # go back and edit the ends on the right of the = once i understand what they do
    N='none'
    HS='high school'
    U='undergrad'
    M = 'masters'
    P = 'phd'
    LEVEL_OF_EDUCATION_CHOICES = (
        (N,'none'),
        (HS,'high school'),
        (U,'undergraduate'),
        (M,'masters'),
        (P,'phd')
    )
    
    education = models.CharField(
        max_length=100,
        choices=LEVEL_OF_EDUCATION_CHOICES,
        default=N
    )


class Article(models.Model):
    placeholder=models.CharField(max_length=150)
    title = models.CharField(max_length=150)
    published_date = models.DateField(default=datetime.date.today())
    content = models.TextField(max_length=100)
    writer = models.ForeignKey('Author',on_delete=models.CASCADE)

    #writer = models.ForeignKey('writer',on_delete=models.CASCADE)
    #    writer = models.ForeignKey(
#        Writer,
#        models.SET_NULL,
#        blank=True,
#        null=True,
#    )

    # ???
    #if writer == nul:
        # b= ? Article?
        # e= entry.object.get 
        # b.entry_set.remove(e)
        
    
    # is this a nullable foreignkey and do I want it to be set null
    # when the reference object is deleted



     #if        
    # should something about article be set to null if author is removed?, so like if
    # the ForeignKey is set null, then 



    

    # should articles disappear if their author is removed?
    #feels like it has to do with recursiveness
    #pass on on_delete option?


    
    # ForeignKey maps to model instances, and defaults should be the value of the field they reference
    # and not the model instance

    # [Article(title='article1',published_date='dhosq'),Article(title='article2',published_date='ddss')]
