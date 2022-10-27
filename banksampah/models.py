from email.policy import default
from random import choices
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

PILIHAN_SAMPAH = (
    ('organik','ORGANIK'),
    ('anorganik', 'ANORGANIK'),
    ('B3','B3'),
)

class Bank(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    jenis = models.CharField(max_length=10, choices=PILIHAN_SAMPAH, default='orgnaik')
    alamat = models.TextField()
    tanggal = models.DateField()
    kontak = models.IntegerField()