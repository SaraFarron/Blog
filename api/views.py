from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from rest_framework.viewsets import ModelViewSet

from BlogApp.models import Post, Comment
from user.models import Guest
from .serializers import PostSerializer, CommentSerializer


class PostViewSet(ModelViewSet):
    """
    Post ViewSet description

    list: List posts

    retrieve: Retrieve post

    update: Update post

    create: Create post

    partial_update: Patch post

    destroy: Delete post
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def create(self, request, *args, **kwargs):
        many = True if isinstance(request.data, list) else False
        serializer = PostSerializer(data=request.data, many=many)
        serializer.is_valid(raise_exception=True)
        author = Guest.objects.get(user=request.user)

        if many:
            post_list = [Post(**data, user=author) for data in serializer.validated_data]
            Post.objects.bulk_create(post_list)

        else:
            post = Post.objects.create(
                name=request.data.get('name'),
                text=request.data.get('text'),
                description=request.data.get('description'),
                user=author
            )
            post.save()

        return Response({}, status=HTTP_201_CREATED)


class CommentViewSet(ModelViewSet):
    """
    Comment ViewSet description

    list: List comments

    retrieve: Retrieve comment

    update: Update comment

    create: Create comment

    partial_update: Patch comment

    destroy: Delete comment
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def create(self, request, *args, **kwargs):
        many = True if isinstance(request.data, list) else False
        serializer = CommentSerializer(data=request.data, many=many)
        serializer.is_valid(raise_exception=True)
        author = Guest.objects.get(user=request.user)
        post = Post.objects.get(id=request.data.get('post'))

        if many:
            post_list = [Comment(**data, author=author) for data in serializer.validated_data]
            Comment.objects.bulk_create(post_list)

        else:
            comment = Comment.objects.create(
                text=request.data.get('text'),
                post=post,
                author=author
            )
            comment.save()

        return Response({}, status=HTTP_201_CREATED)

# TODO override update method
