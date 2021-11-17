from django.db import models
from user.models import Guest


class Post(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, default='Untitled')
    creation_date = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    description = models.TextField(max_length=200)
    user = models.ForeignKey(Guest, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    author = models.ForeignKey(Guest, on_delete=models.CASCADE)
    text = models.TextField()
    publication_date = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    child_comments = models.ManyToManyField('Comment')

    def __str__(self):
        return f"{self.author}'s comment under {self.post.name}"
