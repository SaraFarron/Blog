from django.urls import path
from .views import *


app_name = 'blog'

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('order_by_date', HomeByRating.as_view(), name='home_popular'),
    path('post/<str:pk>/', PostPage.as_view(), {'save': True}, name='post'),
    path('post/<str:pk>/', PostPage.as_view(), {'save': False}, name='post'),

    path('create/', CreatePost.as_view(), name='create'),
    path('update/<str:pk>', UpdatePost.as_view(), name='update'),
    path('delete/<str:pk>', DeletePost.as_view(), name='delete'),

    path('new_comment/<str:pk>', CreateComment.as_view(), name='create_comment'),
    path('reply/<str:post_pk>/<str:comment>', Reply.as_view(), name='reply'),

    path('saved/', SavedContents.as_view(), name='saved')
]
