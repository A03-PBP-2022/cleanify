# Generated by Django 4.1 on 2022-10-27 13:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('banksampah', '0004_alter_bank_kodepos_alter_bank_kota'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bank',
            name='kodepos',
            field=models.CharField(blank=True, max_length=5, null=True),
        ),
        migrations.AlterField(
            model_name='bank',
            name='kota',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]