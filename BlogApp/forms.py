from django.forms import ModelForm
from .models import *


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['name', 'text', 'description']


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
