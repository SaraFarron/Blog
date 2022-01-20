from django.urls import path
from .views import *


app_name = 'user'

urlpatterns = [
    path('login', LoginPage.as_view(), name='login'),
    path('logout', LogoutUser.as_view(), name='logout'),
    path('register', RegisterPage.as_view(), name='register'),
    path('<str:pk>', Profile.as_view(), name='profile'),
    path('<str:pk>/settings', ProfileSettings.as_view(), name='profile_settings'),
]
