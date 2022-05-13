from django.forms import ModelForm, CharField
from .models import Guest
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class ProfileSetForm(ModelForm):

    #name = CharField(disabled=True)
    delete_img=CharField()
    
    class Meta:
        model = Guest
        fields = ['email', 'profile_picture', 'phone', 'skype', 'delete_img']
