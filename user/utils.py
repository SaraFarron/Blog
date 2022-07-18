from datetime import datetime
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


def create_token(user: User) -> Token:
    """
        Creates and saves a token
    :param user: User object
    :return: Token object
    """
    token = Token.objects.create(user=user)
    token.save()
    return token


def seconds_to_formatted_string(time: datetime.__class__) -> str:
    """
        Returns formatted string e.g. '13.5 hours'
    :param time: datetime object
    :return: string
    """
    seconds = time.seconds
    match seconds:
        case seconds if seconds > 86400:
            time = str(time.days) + ' days'
        case seconds if seconds > 3600:
            time = str(round(seconds / 3600)) + ' hours'
        case seconds if seconds > 60:
            time = str(round(seconds / 60)) + ' minutes'
        case _:
            time = str(seconds) + ' seconds'
    return time
