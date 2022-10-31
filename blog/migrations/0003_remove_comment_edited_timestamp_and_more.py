# Generated by Django 4.1 on 2022-10-28 08:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_alter_comment_options_alter_post_options_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='edited_timestamp',
            new_name='modified_timestamp'
        ),
        migrations.RenameField(
            model_name='post',
            old_name='edited_timestamp',
            new_name='modified_timestamp'
        ),
        migrations.AlterField(
            model_name='comment',
            name='modified_timestamp',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='modified_timestamp',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='comment',
            name='created_timestamp',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='created_timestamp',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
