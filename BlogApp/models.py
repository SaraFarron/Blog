from django.db import models
from django.contrib.auth.models import User


class Guest(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    email = models.EmailField()  # can't change
    phone = models.IntegerField()
    profile_picture = models.ImageField(null=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    name = models.CharField(max_length=200, default='Untitled')
    creation_date = models.DateTimeField(auto_now_add=True, null=True)
    text = models.TextField()
    description = models.TextField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name
