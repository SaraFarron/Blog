from django.urls import path
from . import views


app_name = 'user'

urlpatterns = [
    path('login', views.LoginPage.as_view(), name='login'),
    path('logout', views.LogoutUser.as_view(), name='logout'),
    path('register', views.RegisterPage.as_view(), name='register'),
    path('<str:pk>', views.Profile.as_view(), name='profile'),
    path('settings', views.ProfileSettings.as_view(), name='profile_settings'),
]

# TODO create redirect from domain/user
