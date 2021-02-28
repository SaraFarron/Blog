from django.shortcuts import render
from django.http import JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import PostSerializer

from BlogApp.models import Post


@api_view(['GET'])
def api_overview(request):
    api_urls = {
        'list': '/post-list/',
        'detail view': '/post-detail/<str:pk>/',
        'create': '/create/',
        'update': '/update/<str:pk>/',
        'delete': '/delete/<str:pk>/',
    }

    return Response(api_urls)


@api_view(['GET'])
def post_list(request):
    posts = Post.objects.all().order_by('-id')
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def post_detail(request, pk):
    posts = Post.objects.get(id=pk)
    serializer = PostSerializer(posts, many=False)
    return Response(serializer.data)


@api_view(['POST'])
def post_create(request):
    serializer = PostSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['POST'])
def post_update(request, pk):
    post = Post.objects.get(id=pk)
    serializer = PostSerializer(instance=post, data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['DELETE'])
def post_delete(request, pk):
    post = Post.objects.get(id=pk)
    post.delete()

    return Response('Item successfully delete!')
