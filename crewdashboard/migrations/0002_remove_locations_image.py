# Generated by Django 4.1 on 2022-11-01 03:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crewdashboard', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='locations',
            name='image',
        ),
    ]
