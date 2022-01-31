from rest_framework.mixins import CreateModelMixin, ListModelMixin, DestroyModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_200_OK, HTTP_403_FORBIDDEN
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from .serializers import *


def update_user_rating(user):
    posts = Post.objects.filter(user=user)
    comments = Comment.objects.filter(user=user)
    posts_rating = sum([post.rating for post in posts])
    comments_rating = sum([comment.rating for comment in comments])
    user.rating = posts_rating + comments_rating
    user.save()


class RateModelMixin:
    """
        Update a model instance.
    """

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        action = request.data['rating']
        user = Guest.objects.get(user=request.user)
        upvoted_users_query = instance.upvoted_users
        downvoted_users_query = instance.downvoted_users
        instance_user = instance.user

        match action:
            case 'upvote':
                if user not in upvoted_users_query.all():
                    upvoted_users_query.add(user)
                    if user in downvoted_users_query.all():
                        downvoted_users_query.remove(user)
                else:
                    Response({'error': 'You already upvoted this'}, status=HTTP_403_FORBIDDEN)
            case 'downvote':
                if user not in downvoted_users_query.all():
                    downvoted_users_query.add(user)
                    if user in upvoted_users_query.all():
                        upvoted_users_query.remove(user)
                else:
                    Response({'error': 'You already downvoted this'}, status=HTTP_403_FORBIDDEN)
            case _:
                return Response(status=HTTP_403_FORBIDDEN)

        instance.rating = len(upvoted_users_query.all()) - len(downvoted_users_query.all())
        instance.save()
        update_user_rating(instance_user)
        return Response(status=HTTP_200_OK)


class ActionBasedPermission(AllowAny):
    """
        Grant or deny access to a view, based on a mapping in view.action_permissions
    """
    def has_permission(self, request, view):
        for klass, actions in getattr(view, 'action_permissions', {}).items():
            if view.action in actions:
                return klass().has_permission(request, view)
        return False


def set_default_permissions():
    permission_classes = (ActionBasedPermission,)
    action_permissions = {
        IsAuthenticated: ['update', 'partial_update', 'destroy', 'create'],
        AllowAny: ['list', 'retrieve']
    }
    return permission_classes, action_permissions


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

    def create(self, request, *args, **kwargs):
        many = True if isinstance(request.data, list) else False
        serializer = CommentSerializer(data=request.data, many=many)
        serializer.is_valid(raise_exception=True)
        author = Guest.objects.get(user=request.user)
        post = Post.objects.get(id=request.data.get('post'))

        if many:
            post_list = [Comment(**data, author=author) for data in serializer.validated_data]
            Comment.objects.bulk_create(post_list)

        elif 'parent_comment' in request.data.keys():
            parent_comment = Comment.objects.get(id=request.data.get('parent_comment'))
            comment = Comment.objects.create(
                text=request.data.get('text'),
                post=post,
                user=author
            )
            comment.save()
            parent_comment.replies.add(comment)
            parent_comment.save()

        else:
            comment = Comment.objects.create(
                text=request.data.get('text'),
                post=post,
                user=author
            )
            comment.save()

        return Response({}, status=HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        comments = Comment.objects.all()
        replies = []
        for comment in comments:
            replies += list(comment.replies.all())
        for reply in replies:
            comments = comments.exclude(id=reply.id)
        queryset = comments

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

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        user = Guest.objects.get(user=request.user)
        saved_by_query = instance.saved_by

        if user in saved_by_query.all():
            saved_by_query.remove(user)
        else:
            saved_by_query.add(user)
        instance.save()
        return Response(status=HTTP_200_OK)


class SavePostView(SaveModelMixin, GenericViewSet):
    """
        Save post
    """
    queryset = Post.objects.all()
    # serializer_class = PostSerializer


class SaveCommentView(SaveModelMixin, GenericViewSet):
    """
        Save comment
    """
    queryset = Comment.objects.all()
    # serializer_class = CommentSerializer
