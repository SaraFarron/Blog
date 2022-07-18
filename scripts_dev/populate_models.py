from uuid import uuid4
from faker import Faker
import random

from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from BlogApp.models import Comment, Post
from user.models import Guest
from user.utils import create_token


def populate_users(n: int) -> None:
    fake = Faker()
    for i in range(n):
        username = fake.user_name()
        try:
            user = User.objects.create(
                    username=username,
                    password=uuid4().hex,
                    email=f'{username}@gmail.com'
                )
            user.save()
        except IntegrityError:
            print('User already exists')
            continue
        token = create_token(user)
        guest = Guest.objects.create(
                user=user,
                name=username,
                token=token.key,
                email=f'{username}@gmail.com'
            )
        guest.save()


def populate_posts(n: int) -> None:
    fake = Faker()
    users = list(Guest.objects.all())
    users = random.sample(users, n)
    for i in range(n):
        user = random.choice(users)
        post = Post.objects.create(
            user=user,
            name=' '.join(fake.words()),
            description=fake.paragraph(),
            text=''.join(fake.texts(5))
        )
        post.save()


def populate_comments(n: int) -> None:
    fake = Faker()
    users = list(Guest.objects.all())
    users = random.sample(users, n)
    posts = list(Post.objects.all())
    posts = random.sample(posts, n)
    for i in range(n):
        user = random.choice(users)
        post = random.choice(posts)
        comment = Comment.objects.create(
            user=user,
            post=post,
            text=''.join(fake.texts(2))
        )
        post.number_of_comments = Comment.objects.filter(post=post).count() + 1
        comment.save()
        post.save()
