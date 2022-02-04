# Generated by Django 4.0.1 on 2022-02-02 05:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_alter_guest_name_alter_guest_user'),
        ('BlogApp', '0004_post_number_of_comments'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='downvoted_users',
            field=models.ManyToManyField(blank=True, related_name='downvoted_comment_users', to='user.Guest', verbose_name='downvoted by'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='upvoted_users',
            field=models.ManyToManyField(blank=True, related_name='upvoted_comment_users', to='user.Guest', verbose_name='upvoted by'),
        ),
        migrations.AlterField(
            model_name='post',
            name='downvoted_users',
            field=models.ManyToManyField(blank=True, related_name='downvoted_post_users', to='user.Guest', verbose_name='downvoted by'),
        ),
        migrations.AlterField(
            model_name='post',
            name='upvoted_users',
            field=models.ManyToManyField(blank=True, related_name='upvoted_post_users', to='user.Guest', verbose_name='upvoted by'),
        ),
    ]