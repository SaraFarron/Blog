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


# class CreateUserForm(UserCreationForm):
#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password1', 'password2']
#
#
# class ProfileSetForm(ModelForm):
#     class Meta:
#         model = Guest
#         fields = ['name', 'profile_picture', 'phone', 'skype']
