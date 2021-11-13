from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import APIView
from BlogApp.models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from drf_yasg.utils import swagger_auto_schema
from user.models import Guest

from rest_framework.viewsets import ModelViewSet


class TestViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class Comments(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        query_serializer=CommentSerializer(),
        responses={
            status.HTTP_200_OK: CommentSerializer()
        }
    )
    def get(self, request):
        """List of all comments on certain post"""

        post_id = request.data.get('post')

        try:
            post = Post.objects.get(id=post_id)

        except ObjectDoesNotExist:
            return Response(
                {'error': f'did not find post {post_id}'},
                status=404
            )
        comments = Comment.objects.filter(post=post)
        serializer = CommentSerializer(data=comments, many=True)

        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=200)

    @swagger_auto_schema(
        request_body=CommentSerializer(),
        responses={
            status.HTTP_200_OK: CommentSerializer()
        }
    )
    def post(self, request):
        """Create a comment under a certain post. With comment parameter reply to comment"""

        post_id = request.data.get('post')
        comment_id = request.data.get('comment')

        try:
            post = Post.objects.get(id=post_id)

        except ObjectDoesNotExist:
            return Response(
                {'error': f'did not find post {post_id}'},
                status=404
            )
        user = Guest.objects.get(user=request.user)

        if type(comment_id) is int:
            comment = Comment.objects.create(
                author=user,
                text=request.data.get('text'),
                post=None
            )
            comment.save()
            parent_comment = Comment.objects.get(id=comment_id)
            parent_comment.child_comments.add(comment)
            parent_comment.save()
            return Response(status=200)
        comment = Comment.objects.create(
            author=user,
            text=request.data.get('text'),
            post=post
        )
        comment.save()
        return Response(status=200)


class Posts(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        query_serializer=PostSerializer(),
        responses={
            status.HTTP_200_OK: PostSerializer()
        }
    )
    def get(self, request):
        """Get a certain post or list of all posts if without post parameter"""

        post_id = request.data.get('post')

        if type(post_id) is int:
            posts = Post.objects.get(id=post_id)

        else:
            posts = Post.objects.all().order_by('-id')
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=200)

    @swagger_auto_schema(
        request_body=PostSerializer(),
        responses={
            status.HTTP_200_OK: PostSerializer()
        }
    )
    def post(self, request):
        """Create a post"""

        name = request.data.get('name')
        text = request.data.get('text')
        description = request.data.get('description')
        user = Guest.objects.get(user=request.user)

        try:
            post = Post.objects.create(
                name=name,
                text=text,
                description=description,
                user=user
            )
            post.save()

            return Response(status=200)
        except ValueError or AttributeError:
            return Response({'error': 'bad data was sent'}, status=400)


class ApiOverview(APIView):

    def get(self, request):
        api_urls = {
            'posts': '/posts/',
            'comments': '/comments/',
            'post-update': '/update/<str:pk>/',
            'post-delete': '/delete/<str:pk>/',
        }
        return Response(api_urls, status=200)


class PostUpdate(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=PostSerializer(),
        responses={
            status.HTTP_200_OK: PostSerializer()
        }
    )
    def post(self, request):
        """Update post"""

        post = Post.objects.get(id=request.data.get('post'))

        if post.user != request.user:
            return Response({'error': 'cannot edit posts that are not yours'}, status=403)
        serializer = PostSerializer(instance=post, data=request.data)

        if serializer.is_valid():
            serializer.save()

        return Response(serializer.data, status=200)


class PostDelete(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=PostSerializer(),
        responses={
            status.HTTP_200_OK: PostSerializer()
        }
    )
    def delete(self, request):
        """Delete one post"""

        post = Post.objects.get(id=request.data.get('post'))

        if post.user != request.user:
            return Response({'error': 'cannot edit posts that are not yours'}, status=403)
        post.delete()

        return Response('Item successfully deleted!', status=200)
