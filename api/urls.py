from django.urls import path
from django.conf.urls import include
from rest_framework.routers import DefaultRouter
from .views import *


router = DefaultRouter()
router.register(r'posts', PostViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'users', UsersViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('posts/rate/<int:id>', RatePostView.as_view()),
    path('posts/save/<int:id>/', SavePostView.as_view()),
    path('comments/rate/<int:id>', RateCommentView.as_view()),
    path('comments/save/<int:id>', SaveCommentView.as_view()),
]
