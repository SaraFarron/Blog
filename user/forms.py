from django.forms import ModelForm, CharField
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from phonenumber_field.formfields import PhoneNumberField

from .models import Guest


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class ProfileSetForm(ModelForm):

    delete_img=CharField()
    phone = PhoneNumberField()
    
    class Meta:
        model = Guest
        fields = ['email', 'profile_picture', 'phone', 'skype', 'delete_img']
