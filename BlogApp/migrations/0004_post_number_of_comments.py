# Generated by Django 4.0.1 on 2022-02-01 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BlogApp', '0003_remove_post_number_of_comments'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='number_of_comments',
            field=models.IntegerField(default=0, verbose_name='number of comments'),
        ),
    ]