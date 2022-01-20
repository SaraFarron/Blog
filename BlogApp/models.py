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
    upvoted_users = models.ManyToManyField(Guest, related_name='upvoted_post_users')
    downvoted_users = models.ManyToManyField(Guest, related_name='downvoted_post_users')
    number_of_comments = models.IntegerField(default=0, verbose_name=_('number of comments'))

    def __str__(self):
        return self.name


class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    author = models.ForeignKey(Guest, on_delete=models.CASCADE, verbose_name=_('author'))
    text = models.TextField(verbose_name=_('text'))
    publication_date = models.DateTimeField(auto_now_add=True, verbose_name=_('publication date'))
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name=_('post name'))
    replies = models.ManyToManyField('Comment', verbose_name=_('replies'))
    rating = models.IntegerField(default=0, verbose_name=_('rating'))
    upvoted_users = models.ManyToManyField(Guest, related_name='upvoted_comment_users')
    downvoted_users = models.ManyToManyField(Guest, related_name='downvoted_comment_users')

    def __str__(self):
        return f"{self.author}" + _("'s comment")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.post.number_of_comments += 1
