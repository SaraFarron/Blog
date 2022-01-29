from django.db.models import QuerySet
from rest_framework.mixins import CreateModelMixin, ListModelMixin, DestroyModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_200_OK
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from .serializers import *


class PatchModelMixin:
    """
    Update a model instance.
    """

    def partial_update(self, request, *args, **kwargs):
        partial = True
        instance = self.queryset.get(pk=kwargs['pk'])
        # instance = self.get_object()
        instance.rating += 1
        instance.user.rating += 1
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()


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


class CastVote:
    queryset = None
    serializer_class = None
    permission_classes = (ActionBasedPermission,)
    action_permissions = {
        IsAuthenticated: ['update', 'partial_update', 'destroy', 'create'],
        AllowAny: ['list', 'retrieve']
    }

    def patch(self, request, *args, **kwargs):
        query = self.get_queryset()
        if query is Post:
            query = query.objects.get(kwargs['post'])
        elif query is Comment:
            query = query.objects.get(kwargs['comment'])
        user = request.user
        vote = kwargs['vote']
        if vote == 'upvote' and user not in query.upvoted_users.all():
            query.rating += 1
            query.upvoted_users.add(user)
            response = Response(status=200)
        elif vote == 'downvote' and user not in query.downvoted_users.all():
            query.rating -= 1
            query.downvoted_users.add(user)
            response = Response(status=200)
        else:
            response = Response(status=400)
        serializer = self.serializer_class(query, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response

    def get_queryset(self):
        """
        Get the list of items for this view.
        This must be an iterable, and may be a queryset.
        Defaults to using `self.queryset`.

        This method should always be used rather than accessing `self.queryset`
        directly, as `self.queryset` gets evaluated only once, and those results
        are cached for all subsequent requests.

        You may want to override this if you need to provide different
        querysets depending on the incoming request.

        (Eg. return a list of items that is specific to the user)
        """
        assert self.queryset is not None, (
            "'%s' should either include a `queryset` attribute, "
            "or override the `get_queryset()` method."
            % self.__class__.__name__
        )

        queryset = self.queryset
        if isinstance(queryset, QuerySet):
            # Ensure queryset is re-evaluated on each request.
            queryset = queryset.all()
        return queryset


class RatePostView(PatchModelMixin, GenericViewSet):
    """
    Rate a post
    """
    serializer_class = RatePostSerializer
    queryset = Post.objects.all()


class RateCommentView(PatchModelMixin, GenericViewSet):
    """
    Rate a comment
    """
    queryset = Comment.objects.all()
    serializer_class = RateCommentSerializer


class Save:
    queryset = None
    permission_classes, action_permissions = set_default_permissions()

    def patch(self, request, id):
        """Toggle save"""
        query = self.queryset.objects.get(id=id)
        users = query.saved_by
        user = request.user
        if user not in users:
            query.saved_by.add(user)
        else:
            query.saved_by.remove(user)
        query.save()
        return Response(status=HTTP_200_OK)


class SavePostView(PatchModelMixin, GenericViewSet):
    """Save post"""
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class SaveCommentView(PatchModelMixin, GenericViewSet):
    """Save comment"""
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
