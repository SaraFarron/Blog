from django.db import models
from django.contrib.auth.models import User


class Guest(models.Model):

    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)  # should be unique
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    email = models.EmailField(default='example@blog.com')  # can't change
    phone = models.IntegerField(blank=True, default=111111)
    profile_picture = models.ImageField(null=True, blank=True)
    skype = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    
    name = models.CharField(max_length=200, default='Untitled')
    creation_date = models.DateTimeField(auto_now_add=True, null=True)
    text = models.TextField()
    description = models.TextField(max_length=200)
    user = models.ForeignKey(Guest, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name


class Comment(models.Model):

    author = models.ForeignKey(Guest, on_delete=models.CASCADE)
    text = models.TextField()
    publication_date = models.DateTimeField(auto_now_add=True, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.author}'s comment under {self.post.name}"
