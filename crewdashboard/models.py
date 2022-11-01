from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

class Locations(models.Model):
    date= models.DateField(auto_now_add=True)
    location = models.CharField(max_length=200, null=True)
    urgency= models.IntegerField(
        null =True, 
        validators=[
            MaxValueValidator(5),
            MinValueValidator(1)
        ])
    description= models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title