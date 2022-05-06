from typing import Literal
from django.db.models import QuerySet
from rest_framework.status import HTTP_403_FORBIDDEN, HTTP_200_OK
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from silk.profiling.profiler import silk_profile
from BlogApp.models import Post, Comment, Guest


@silk_profile(name='update user func')
def update_user_rating(user: Guest) -> None:
    """
        Updates user's rating
    :param user: Guest instance
    :return: None
    """
    posts = Post.objects.filter(user=user)
    comments = Comment.objects.filter(user=user)
    posts_rating = sum([post.rating for post in posts])
    comments_rating = sum([comment.rating for comment in comments])
    user.rating = posts_rating + comments_rating
    user.save()


@silk_profile(name='update instance func')
def update_instance_rating(instance: Comment | Post, user: Guest, action: Literal['upvote', 'downvote']) -> Response:
    """
        Update rating of instance and it's owner, return 200 or 403
    :param instance: Comment or Post instance
    :param user: Guest instance
    :param action: either 'upvote' or 'downvote'
    :return: Response object
    """
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
            return Response({'error': f'{instance.__str__()} can only be upvoted or downvoted'},
                            status=HTTP_403_FORBIDDEN)
    instance.rating = upvoted_users_query.all().count() - downvoted_users_query.all().count()
    instance.save()
    update_user_rating(instance_user)
    return Response(status=HTTP_200_OK)


def toggle_save_instance(instance: Comment | Post, user: Guest) -> Response:
    saved_by_query = instance.saved_by

    if user in saved_by_query.all():
        saved_by_query.remove(user)
    else:
        saved_by_query.add(user)
    instance.save()
    return Response(status=HTTP_200_OK)


@silk_profile(name='get comments func')
def get_comments_with_replies(post=None) -> QuerySet:
    """
        Returns queryset with comments and replies without repeating
    :param post: Post object, if provided will return only comments related to post
    :return: QuerySet object
    """
    if post:
        comments = Comment.objects.filter(post=post).prefetch_related('replies', 'user', 'post')
    else:
        comments = Comment.objects.prefetch_related('replies', 'user', 'post')
    replies = []
    for c in comments:
        replies += sorted(c.replies.all(), key=lambda d: d.publication_date, reverse=True)
    for reply in replies:
        comments = comments.exclude(id=reply.id)
    return comments


@silk_profile(name='create reply func')
def create_reply(post: Post, user: Guest, text: str, parent_comment_id: int) -> None:
    """
        Creates a reply and updates parent comment
    :param post: Post object
    :param user: Guest object
    :param text: String
    :param parent_comment_id: Integer
    :return: None
    """
    parent_comment = Comment.objects.get(id=parent_comment_id)
    comment = Comment.objects.create(
        text=text,
        post=post,
        user=user
    )
    comment.save()
    parent_comment.replies.add(comment)
    parent_comment.save()


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
