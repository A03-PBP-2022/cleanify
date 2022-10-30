from django.db import models

# Create your models here.
class FAQ(models.Model) :
    question = models.CharField(max_length=400)
    answer = models.TextField()
    thumbsUp = models.IntegerField(default=0)
