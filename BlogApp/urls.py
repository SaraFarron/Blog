from django.urls import path
from . import views


app_name = 'Blog'
urlpatterns = [
    path('', views.index, name='home'),

    path('create/', views.create_post, name='create'),
    path('update/<str:pk>', views.update_post, name='update'),
    path('delete/<str:pk>', views.delete_post, name='delete'),

    path('login', views.login_page, name='login'),
    path('logout', views.logout_user, name='logout'),
    path('register', views.register_page, name='register'),
]
