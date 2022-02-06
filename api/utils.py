from typing import Literal
from rest_framework.status import HTTP_403_FORBIDDEN, HTTP_200_OK
from rest_framework.response import Response
from BlogApp.models import Post, Comment, Guest


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
    instance.rating = len(upvoted_users_query.all()) - len(downvoted_users_query.all())
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
