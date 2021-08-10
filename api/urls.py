from django.urls import path
from . import views


urlpatterns = [
    path('', views.ApiOverview.as_view(), name="api-overview"),
    path('posts', views.Posts.as_view(), name="posts"),
    path('comments', views.Comments.as_view(), name='comments'),

    path('post-update/<str:pk>', views.PostUpdate.as_view(), name="post-update"),
    path('post-delete/<str:pk>', views.PostDelete.as_view(), name="post-delete"),
]
