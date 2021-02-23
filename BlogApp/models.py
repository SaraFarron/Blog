from django.db import models
from django.contrib.auth.models import User


class Guest(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    email = models.EmailField(default='example@blog.com')  # can't change
    phone = models.IntegerField(null=True)
    profile_picture = models.ImageField(null=True)
    skype = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    """TODO Users can leave comments under posts
    (cannot comment your own post)"""
    name = models.CharField(max_length=200, default='Untitled')
    creation_date = models.DateTimeField(auto_now_add=True, null=True)
    text = models.TextField()
    description = models.TextField(max_length=200)
    user = models.ForeignKey(Guest, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name
