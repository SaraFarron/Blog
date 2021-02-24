from django.urls import path
from . import views


app_name = 'Blog'
urlpatterns = [
    path('', views.index, name='home'),
    path('post/<str:pk>', views.post_page, name='post'),

    path('create/', views.create_post, name='create'),
    path('update/<str:pk>', views.update_post, name='update'),
    path('delete/<str:pk>', views.delete_post, name='delete'),

    path('new_comment/<str:pk>', views.create_comment, name='create_comment'),

    path('login', views.login_page, name='login'),
    path('logout', views.logout_user, name='logout'),
    path('register', views.register_page, name='register'),
    path('user/<str:pk>', views.profile, name='profile'),
]
