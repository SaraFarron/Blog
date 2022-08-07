from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField


class Guest(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, unique=True, null=True, verbose_name=_('name'))
    date_created = models.DateTimeField(auto_now_add=True, null=True, verbose_name='registration date')
    email = models.EmailField(default='example@blog.com', verbose_name=_('email'))
    phone = PhoneNumberField(null=True, blank=True, verbose_name=_('phone'))
    profile_picture = models.CharField(max_length=256, null=True, blank=True, default=None, verbose_name=_('profile picture'))
    skype = models.CharField(max_length=50, null=True, blank=True)
    token = models.CharField(max_length=256, unique=True, null=True, verbose_name=_('token'))
    is_moderator = models.BooleanField(default=False, verbose_name=_('moderation status'))
    is_banned = models.BooleanField(default=False, verbose_name=_('is banned'))
    is_muted = models.BooleanField(default=False, verbose_name=_('is muted'))
    last_ban_date = models.DateTimeField(null=True, blank=True, verbose_name=_('last ban date'))
    rating = models.IntegerField(default=0, verbose_name=_('rating'))

    def __str__(self):
        return self.name
