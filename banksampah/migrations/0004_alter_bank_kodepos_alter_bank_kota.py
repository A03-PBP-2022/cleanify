# Generated by Django 4.1 on 2022-10-27 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('banksampah', '0003_alter_bank_kodepos_alter_bank_kota'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bank',
            name='kodepos',
            field=models.CharField(default='SOME STRING', max_length=5),
        ),
        migrations.AlterField(
            model_name='bank',
            name='kota',
            field=models.CharField(default='SOME STRING', max_length=15),
        ),
    ]
