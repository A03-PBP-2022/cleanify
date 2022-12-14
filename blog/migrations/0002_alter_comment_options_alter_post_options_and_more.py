# Generated by Django 4.1 on 2022-10-28 06:00

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'permissions': [('create_comment', 'Can create new comments'), ('edit_self_comment', 'Can edit comments made by the user'), ('edit_other_comment', 'Can edit comments made by other users'), ('delete_self_comment', 'Can delete comments made by the user'), ('delete_other_comment', 'Can delete comments made by other users')]},
        ),
        migrations.AlterModelOptions(
            name='post',
            options={'permissions': [('create_post', 'Can create new posts'), ('edit_self_post', 'Can edit posts made by the user'), ('edit_other_post', 'Can edit posts made by other users'), ('delete_self_post', 'Can delete posts made by the user'), ('delete_other_post', 'Can delete posts made by other users')]},
        ),
        migrations.RenameField(
            model_name='comment',
            old_name='timestamp',
            new_name='created_timestamp',
        ),
        migrations.RenameField(
            model_name='post',
            old_name='timestamp',
            new_name='created_timestamp',
        ),
        migrations.AddField(
            model_name='comment',
            name='edited_timestamp',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='post',
            name='edited_timestamp',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
