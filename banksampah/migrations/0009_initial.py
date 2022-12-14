# Generated by Django 4.1 on 2022-11-02 05:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('banksampah', '0008_bank_user'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Bank',
        ),
        migrations.CreateModel(
            name='Bank',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('jenis', models.CharField(max_length=10)),
                ('alamat', models.TextField(max_length=100)),
                ('tanggal', models.DateField()),
                ('kontak', models.CharField(max_length=12)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
