from django.db import models
# Create your models here.

PILIHAN_SAMPAH = (
    ('organik','Organik'),
    ('anorganik', 'Anorganik'),
    ('B3','B3'),
)

class Bank(models.Model):
    jenis = models.CharField(max_length=10)
    alamat = models.TextField(max_length=100)
    tanggal = models.DateField()
    kontak = models.CharField(max_length=12)