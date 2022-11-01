from django.db import models
# from django.contrib.auth.models import User
from authc.models import User
# Create your models here.

PILIHAN_SAMPAH = (
    ('organik','Organik'),
    ('anorganik', 'Anorganik'),
    ('B3','B3'),
)

class Bank(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    jenis = models.CharField(max_length=10)
    alamat = models.TextField(max_length=100)
    tanggal = models.DateField()
    kontak = models.CharField(max_length=12)