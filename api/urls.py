from django.urls import path
from django.conf.urls import include
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()
router.register(r'posts', views.PostViewSet)
router.register(r'comments', views.CommentViewSet)
router.register(r'users', views.UsersViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
