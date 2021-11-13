from django.urls import path
from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from . import views


# router = DefaultRouter()
# router.register(r'test', views.TestViewSet)

urlpatterns = [
    path('', views.ApiOverview.as_view(), name="api-overview"),
    path('posts', views.Posts.as_view(), name="posts"),
    path('comments', views.Comments.as_view(), name='comments'),

    path('post-update', views.PostUpdate.as_view(), name="post-update"),
    path('post-delete', views.PostDelete.as_view(), name="post-delete"),
    # path(r'test', views.TestViewSet, name='test'),
]
