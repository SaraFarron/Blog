from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.exceptions import ObjectDoesNotExist
from BlogApp.models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from user.models import Guest


class Comments(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_post(self, post_id):
        try:
            post = Post.objects.get(id=post_id)
        except ObjectDoesNotExist:
            return Response(
                {'error': f'did not find post {post_id}'},
                status=404
            )  # Bug: this returns to method, not to user
        return post

    def get(self, request):
        post_id = request.data.get('post')
        post = self.get_post(post_id)
        comments = Comment.objects.filter(post=post)
        serializer = CommentSerializer(data=comments, many=True)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=200)

    def post(self, request):
        post_id = request.data.get('post')
        comment_id = request.data.get('comment')
        post = self.get_post(post_id)
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

    def get(self, request):
        post_id = request.data.get('post')
        if type(post_id) is int:
            posts = Post.objects.get(id=post_id)
        else:
            posts = Post.objects.all().order_by('-id')
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def post(self, request):
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
        return Response(api_urls)


class PostUpdate(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        post = Post.objects.get(id=pk)
        serializer = PostSerializer(instance=post, data=request.data)

        if serializer.is_valid():
            serializer.save()

        return Response(serializer.data)


class PostDelete(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        post = Post.objects.get(id=pk)
        post.delete()

        return Response('Item successfully deleted!')
