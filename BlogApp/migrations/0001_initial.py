# Generated by Django 4.0.1 on 2022-01-29 14:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(default='Untitled', max_length=200, verbose_name='name')),
                ('creation_date', models.DateTimeField(auto_now_add=True, verbose_name='creation date')),
                ('text', models.TextField(verbose_name='text')),
                ('description', models.TextField(max_length=200, verbose_name='description')),
                ('rating', models.IntegerField(default=0, verbose_name='rating')),
                ('number_of_comments', models.IntegerField(default=0, verbose_name='number of comments')),
                ('downvoted_users', models.ManyToManyField(related_name='downvoted_post_users', to='user.Guest')),
                ('saved_by', models.ManyToManyField(related_name='post_saved_by', to='user.Guest', verbose_name='post saved by')),
                ('upvoted_users', models.ManyToManyField(related_name='upvoted_post_users', to='user.Guest')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='user.guest', verbose_name='author')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('text', models.TextField(verbose_name='text')),
                ('publication_date', models.DateTimeField(auto_now_add=True, verbose_name='publication date')),
                ('rating', models.IntegerField(default=0, verbose_name='rating')),
                ('downvoted_users', models.ManyToManyField(related_name='downvoted_comment_users', to='user.Guest')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='BlogApp.post', verbose_name='post name')),
                ('replies', models.ManyToManyField(to='BlogApp.Comment', verbose_name='replies')),
                ('saved_by', models.ManyToManyField(related_name='comment_saved_by', to='user.Guest', verbose_name='comment saved by')),
                ('upvoted_users', models.ManyToManyField(related_name='upvoted_comment_users', to='user.Guest')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.guest', verbose_name='author')),
            ],
        ),
    ]
