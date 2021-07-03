from django.urls import path
from . import views


app_name = 'blog'

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('order_by_date', views.HomeByDate.as_view(), name='home_by_date'),
    path('post/<str:pk>', views.PostPage.as_view(), name='post'),

    path('create/', views.CreatePost.as_view(), name='create'),
    path('update/<str:pk>', views.UpdatePost.as_view(), name='update'),
    path('delete/<str:pk>', views.DeletePost.as_view(), name='delete'),

    path('new_comment/<str:pk>', views.CreateComment.as_view(), name='create_comment'),

    path('login', views.LoginPage.as_view(), name='login'),
    path('logout', views.LogoutUser.as_view(), name='logout'),
    path('register', views.RegisterPage.as_view(), name='register'),
    path('user/<str:pk>', views.Profile.as_view(), name='profile'),
    path('settings', views.ProfileSettings.as_view(), name='profile_settings'),
]