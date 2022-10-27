from django.db import models
# Create your models here.

PILIHAN_SAMPAH = (
    ('organik','ORGANIK'),
    ('anorganik', 'ANORGANIK'),
    ('B3','B3'),
)

class Bank(models.Model):
    jenis = models.CharField(max_length=10, choices=PILIHAN_SAMPAH, default='orgnaik')
    alamat = models.TextField(max_length=100)
    tanggal = models.DateField()
    kontak = models.CharField(max_length=12)