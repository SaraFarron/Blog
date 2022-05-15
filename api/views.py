from rest_framework.mixins import CreateModelMixin, ListModelMixin, DestroyModelMixin, RetrieveModelMixin
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from silk.profiling.profiler import silk_profile
from .serializers import *
from .utils import update_instance_rating, toggle_save_instance, get_comments_with_replies, create_reply, \
    set_default_permissions


class RateModelMixin:
    """
        Update a model instance.
    """
    @silk_profile(name='Rate Mixin')
    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        action = request.data['rating']
        user = Guest.objects.get(user=request.user)
        return update_instance_rating(instance, user, action)


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
    permission_classes, action_permissions = set_default_permissions()

    @silk_profile(name='Post Create')
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


class CommentViewSet(CreateModelMixin, ListModelMixin, DestroyModelMixin, GenericViewSet):
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
    permission_classes, action_permissions = set_default_permissions()

    @silk_profile(name='Comment Create')
    def create(self, request, *args, **kwargs):
        many = True if isinstance(request.data, list) else False
        serializer = CommentSerializer(data=request.data, many=many)
        serializer.is_valid(raise_exception=True)
        user = Guest.objects.get(user=request.user)
        post = Post.objects.get(id=request.data.get('post'))
        comment_text = request.data.get('text')

        if many:
            post_list = [Comment(**data, user=user) for data in serializer.validated_data]
            Comment.objects.bulk_create(post_list)
        elif 'parent_comment' in request.data.keys():
            parent_comment_id = request.data.get('parent_comment')
            create_reply(post, user, comment_text, parent_comment_id)
        else:
            comment = Comment.objects.create(
                text=comment_text,
                post=post,
                user=user,
                owner_id=user.id
            )
            comment.save()

        post.number_of_comments = Comment.objects.filter(post=post).count() + 1
        post.save()
        return Response(status=HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        queryset = get_comments_with_replies()

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class UsersViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    """
        list: List users

        retrieve: Retrieve user
    """
    queryset = Guest.objects.all()
    serializer_class = UserSerializer
    permission_classes, action_permissions = set_default_permissions()


class RatePostView(RateModelMixin, GenericViewSet):
    """
        Rate a post
    """
    serializer_class = RatePostSerializer
    queryset = Post.objects.all()


class RateCommentView(RateModelMixin, GenericViewSet):
    """
        Rate a comment
    """
    queryset = Comment.objects.all()
    serializer_class = RateCommentSerializer


class SaveModelMixin:

    @silk_profile(name='Save Mixin')
    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        user = Guest.objects.get(user=request.user)

        return toggle_save_instance(instance, user)


class SavePostView(SaveModelMixin, GenericViewSet):
    """
        Save post
    """
    queryset = Post.objects.all()


class SaveCommentView(SaveModelMixin, GenericViewSet):
    """
        Save comment
    """
    queryset = Comment.objects.all()
