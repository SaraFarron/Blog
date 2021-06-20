from rest_framework.response import Response
from rest_framework.views import APIView

from BlogApp.models import Post
from .serializers import PostSerializer


class ApiOverview(APIView):
    def get(self, request):
        api_urls = {
            'list': '/post-list/',
            'detail view': '/post-detail/<str:pk>/',
            'create': '/create/',
            'update': '/update/<str:pk>/',
            'delete': '/delete/<str:pk>/',
        }

        return Response(api_urls)


class PostList(APIView):
    def get(self, request):
        posts = Post.objects.all().order_by('-id')
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)


class PostDetail(APIView):
    def get(self, request, pk):
        posts = Post.objects.get(id=pk)
        serializer = PostSerializer(posts, many=False)
        return Response(serializer.data)


class PostCreate(APIView):
    def post(self, request):
        serializer = PostSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

        return Response(serializer.data)


class PostUpdate(APIView):
    def post(self, request, pk):
        post = Post.objects.get(id=pk)
        serializer = PostSerializer(instance=post, data=request.data)

        if serializer.is_valid():
            serializer.save()

        return Response(serializer.data)


class PostDelete(APIView):
    def delete(self, request, pk):
        post = Post.objects.get(id=pk)
        post.delete()

        return Response('Item successfully delete!')

# TODO Create cool api, not this shit
