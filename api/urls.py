from django.urls import path
from . import views


urlpatterns = [
    path('', views.ApiOverview.as_view(), name="api-overview"),
    path('post-list', views.PostList.as_view(), name="post-list"),
    path('post-detail/<str:pk>', views.PostDetail.as_view(), name="post-detail"),
    path('post-create', views.PostCreate.as_view(), name="post-create"),

    path('post-update/<str:pk>', views.PostUpdate.as_view(), name="post-update"),
    path('post-delete/<str:pk>', views.PostDelete.as_view(), name="post-delete"),
]