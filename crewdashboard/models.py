from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone

class Location(models.Model):
    date= models.DateField(default=timezone.now)
    location = models.CharField(max_length=200, null=True)
    urgency= models.IntegerField(
        null =True, 
        validators=[
            MaxValueValidator(5),
            MinValueValidator(1)
        ])
    description= models.TextField(null=True, blank=True)

    def __str__(self):
        return self.description