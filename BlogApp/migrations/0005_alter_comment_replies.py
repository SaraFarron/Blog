# Generated by Django 4.0.1 on 2022-01-16 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BlogApp', '0004_remove_comment_parent_comment_comment_replies'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='replies',
            field=models.ManyToManyField(to='BlogApp.Comment'),
        ),
    ]
