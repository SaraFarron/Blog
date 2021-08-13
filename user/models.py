from django.db import models
from django.contrib.auth.models import User


class Guest(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    email = models.EmailField(default='example@blog.com')  # can't be change by user
    phone = models.IntegerField(blank=True, default=111111)
    profile_picture = models.ImageField(null=True, blank=True, default='profile.png')
    skype = models.CharField(max_length=50, null=True, blank=True)
    token = models.CharField(max_length=256, unique=True, null=True)

    def __str__(self):
        return self.name
