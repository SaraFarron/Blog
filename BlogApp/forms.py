from django.forms import ModelForm
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['name', 'text', 'description']


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
