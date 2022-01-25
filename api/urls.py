from django.urls import path
from django.conf.urls import include
from rest_framework.routers import DefaultRouter
from .views import *


router = DefaultRouter()
router.register(r'posts', PostViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'users', UsersViewSet)
router.register(r'posts/rate', RatePostView)
router.register(r'comments/rate', RateCommentView)
router.register(r'posts/save', SavePostView)
router.register(r'comments/save', SaveCommentView)

urlpatterns = [
    path('', include(router.urls)),
]
