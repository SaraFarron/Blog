from django.db import models
from user.models import Guest
from django.utils.translation import gettext_lazy as _


class Post(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, default=_('Untitled'), verbose_name=_('name'))
    creation_date = models.DateTimeField(auto_now_add=True, verbose_name=_('creation date'))
    text = models.TextField(verbose_name=_('text'))
    description = models.TextField(max_length=200, verbose_name=_('description'))
    user = models.ForeignKey(Guest, on_delete=models.SET_NULL, null=True, verbose_name=_('author'))
    rating = models.IntegerField(default=0, verbose_name=_('rating'))
    upvoted_users = models.ManyToManyField(Guest, blank=True, related_name='upvoted_post_users',
                                           verbose_name=_('upvoted by'))
    downvoted_users = models.ManyToManyField(Guest, blank=True, related_name='downvoted_post_users',
                                             verbose_name=_('downvoted by'))
    saved_by = models.ManyToManyField(Guest, blank=True, related_name='post_saved_by', verbose_name=_('post saved by'))
    number_of_comments = models.IntegerField(default=0, verbose_name=_('number of comments'))

    def __str__(self):
        return self.name


class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Guest, on_delete=models.CASCADE, verbose_name=_('author'))
    owner_id = models.IntegerField(default=0, verbose_name=_('owner id'))
    owner_pfp_url = models.CharField(blank=True, max_length=256, verbose_name=_('owner pfp url'))
    owner_name = models.CharField(blank=True, max_length=128, verbose_name=_('owner name'))
    owner_is_moderator = models.BooleanField(default=False, verbose_name=_('is owner a mod'))
    text = models.TextField(verbose_name=_('text'))
    publication_date = models.DateTimeField(auto_now_add=True, verbose_name=_('publication date'))
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name=_('post name'))
    replies = models.ManyToManyField('Comment', verbose_name=_('replies'))
    rating = models.IntegerField(default=0, verbose_name=_('rating'))
    upvoted_users = models.ManyToManyField(Guest, blank=True, related_name='upvoted_comment_users',
                                           verbose_name=_('upvoted by'))
    downvoted_users = models.ManyToManyField(Guest, blank=True, related_name='downvoted_comment_users',
                                             verbose_name=_('downvoted by'))
    saved_by = models.ManyToManyField(Guest, blank=True, related_name='comment_saved_by',
                                      verbose_name=_('comment saved by'))

    def __str__(self):
        return f"{self.user}" + _("'s comment")
