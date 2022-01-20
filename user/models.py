from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class Guest(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True, verbose_name=_('name'))
    date_created = models.DateTimeField(auto_now_add=True, null=True, verbose_name='registration date')
    email = models.EmailField(default='example@blog.com', verbose_name=_('email'))
    phone = models.IntegerField(blank=True, default=111111)
    profile_picture = models.ImageField(null=True, blank=True, default='profile.png', verbose_name=_('profile picture'))
    skype = models.CharField(max_length=50, null=True, blank=True)
    token = models.CharField(max_length=256, unique=True, null=True, verbose_name=_('token'))
    is_moderator = models.BooleanField(default=False, verbose_name='moderation status')
    is_banned = models.BooleanField(default=False, verbose_name=_('is banned'))
    is_muted = models.BooleanField(default=False, verbose_name=_('is muted'))
    last_ban_date = models.DateTimeField(null=True, blank=True, verbose_name=_('last ban date'))

    def __str__(self):
        return self.name
