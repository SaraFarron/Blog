from django.urls import path
from . import views

urlpatterns = [
    path('', views.api_overview, name="api-overview"),
    path('post-list/', views.post_list, name="post-list"),
    path('post-detail/<str:pk>/', views.post_detail, name="post-detail"),
    path('post-create/', views.post_create, name="post-create"),

    path('post-update/<str:pk>/', views.post_update, name="post-update"),
    path('post-delete/<str:pk>/', views.post_delete, name="post-delete"),
]
# TODO Fix this abomination
