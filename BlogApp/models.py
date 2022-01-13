from django.db import models
from user.models import Guest
from django.utils.translation import gettext_lazy as _


class Post(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, default=_('Untitled'), verbose_name=_('name'))
    creation_date = models.DateTimeField(auto_now_add=True)
    text = models.TextField(verbose_name=_('text'))
    description = models.TextField(max_length=200, verbose_name=_('description'))
    user = models.ForeignKey(Guest, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name


class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    author = models.ForeignKey(Guest, on_delete=models.CASCADE)  # set null?
    text = models.TextField(verbose_name=_('text'))
    publication_date = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    parent_comment = models.ForeignKey('Comment', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.author}'s comment under {self.post.name}"
