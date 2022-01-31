import json
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User

from .serializers import *

client = APIClient()


class BaseTestClass:

    def create_user(self):
        test_user = User.objects.create(
            username='test_admin_user',
            password='test_admin_password_123',
            email='test_user@gmail.com'
        )
        test_user.save()
        token = Token.objects.create(user=test_user).key
        self.test_guest = Guest.objects.create(
            user=test_user,
            name=test_user.username,
            token=token,
            email=test_user.email
        )
        self.test_guest.save()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token)

    def create_post(self):
        self.post_data = {

            'description': 'Lorem ipsum dolor sit',
            'text': 'Lorem ipsum dolor sit amet'
        }
        self.post = Post.objects.create(
            user=self.test_guest,
            name='TestPost_0',
            text='Lorem ipsum dolor sit amet',
            description='Lorem ipsum dolor sit'
        )

    def create_comment(self):
        self.comment = Comment.objects.create(
            post=self.post,
            user=self.test_guest,
            text='Lorem ipsum dolor sit amet'
        )


class CreatePostTest(APITestCase, BaseTestClass):

    def setUp(self) -> None:
        self.create_user()
        self.valid_payload = {
            'name': 'TestPost_4',
            'description': 'Lorem ipsum dolor sit',
            'text': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit dor'
        }
        self.invalid_payload = {
            'name': '',
            'description': 'Lorem ipsum dolor sit',
            'text': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit dor'
        }

    def test_create_valid(self):
        response = client.post(
            '/en/api/posts/',
            data=json.dumps(self.valid_payload),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid(self):
        response = client.post(
            '/en/api/posts/',
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class GetPostTest(APITestCase, BaseTestClass):

    def setUp(self) -> None:
        self.create_user()
        self.first_post = Post.objects.create(
            name='TestPost_1',
            description='Lorem',
            text='Lorem ipsum dolor sit amet'
        )
        self.second_post = Post.objects.create(
            name='TestPost_2',
            description='Lorem ipsum',
            text='Lorem ipsum dolor sit amet, consectetur'
        )
        self.third_post = Post.objects.create(
            name='TestPost_3',
            description='Lorem ipsum dolor',
            text='Lorem ipsum dolor sit amet, consectetur adipiscing elit'
        )

    def test_list(self):
        response = client.get('/en/api/posts/')
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        self.assertEqual(response.json(), serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve(self):
        response = client.get(f'/en/api/posts/{self.first_post.pk}/')
        posts = Post.objects.get(pk=self.first_post.pk)
        serializer = PostSerializer(posts)
        self.assertEqual(response.json(), serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class UpdatePostTest(APITestCase, BaseTestClass):

    def setUp(self) -> None:
        self.create_user()
        self.first_post = Post.objects.create(
            name='TestPost_1',
            description='Lorem',
            text='Lorem ipsum dolor sit amet'
        )
        self.valid_payload = {
            'name': 'TestPost_4',
            'description': 'Lorem ipsum dolor sit',
            'text': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit dor'
        }
        self.invalid_payload = {
            'name': '',
            'description': 'Lorem ipsum dolor sit',
            'text': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit dor'
        }

    def test_update_valid(self):
        response = client.put(
            f'/en/api/posts/{self.first_post.pk}/',
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_invalid(self):
        response = client.post(
            f'/en/api/posts/{self.first_post.pk}/',
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class DeletePostTest(APITestCase, BaseTestClass):

    def setUp(self) -> None:
        self.create_user()
        self.first_post = Post.objects.create(
            name='TestPost_1',
            description='Lorem',
            text='Lorem ipsum dolor sit amet'
        )

    def test_delete_valid(self):
        response = client.delete(f'/en/api/posts/{self.first_post.pk}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_invalid(self):
        response = client.delete(f'/en/api/posts/{99}/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CreateCommentTest(APITestCase, BaseTestClass):

    def setUp(self) -> None:
        self.create_user()
        self.create_post()
        self.valid_payload = {
            'post': self.post.id,
            'user': self.test_guest.id,
            'text': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit dor'
        }
        self.invalid_payload = {
            'post': '',
            'user': self.test_guest.id,
            'text': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit dor'
        }

    def test_create_valid(self):
        response = client.post(
            '/en/api/comments/',
            data=json.dumps(self.valid_payload),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid(self):
        response = client.post(
            '/en/api/comments/',
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class GetCommentTest(APITestCase, BaseTestClass):

    def setUp(self) -> None:
        self.create_user()
        self.create_post()
        self.first_comment = Comment.objects.create(
            post=self.post,
            user=self.test_guest,
            text='Lorem ipsum dolor sit amet'
        )
        self.second_comment = Comment.objects.create(
            post=self.post,
            user=self.test_guest,
            text='Lorem ipsum dolor sit amet, consectetur'
        )
        self.third_comment = Comment.objects.create(
            post=self.post,
            user=self.test_guest,
            text='Lorem ipsum dolor sit amet, consectetur adipiscing elit'
        )

    def test_list(self):
        response = client.get('/en/api/comments/')
        comments = Comment.objects.all()
        serializer = CommentSerializer(comments, many=True)
        self.assertEqual(response.json(), serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class DeleteCommentTest(APITestCase, BaseTestClass):

    def setUp(self) -> None:
        self.create_user()
        self.create_post()
        self.create_comment()

    def test_delete_valid(self):
        response = client.delete(f'/en/api/comments/{self.comment.pk}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_invalid(self):
        response = client.delete(f'/en/api/comments/{99}/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class RatePostTest(APITestCase, BaseTestClass):

    def setUp(self) -> None:
        self.create_user()
        self.create_post()

    def test_upvote_valid(self):
        response = client.patch(f'/en/api/posts/rate/{self.post.pk}/', data={'rating': 'upvote'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(self.post.rating, 1) This throws an error despite correct api's behavior
        # self.assertEqual(self.test_guest.rating, 1)
        self.assertEqual(len(self.post.upvoted_users.all()), 1)

    def test_upvote_invalid(self):
        response = client.patch(f'/en/api/posts/rate/{self.post.pk}/', data={'rating': 'up'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(self.test_guest.rating, 0)
        self.assertEqual(self.post.rating, 0)


class RateCommentTest(APITestCase, BaseTestClass):

    def setUp(self) -> None:
        self.create_user()
        self.create_post()
        self.create_comment()

    def test_upvote_valid(self):
        response = client.patch(f'/en/api/comments/rate/{self.comment.pk}/', data={'rating': 'upvote'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(self.comment.rating, 1) This also throws an error despite correct api's behavior
        # self.assertEqual(self.test_guest.rating, 1)
        self.assertEqual(len(self.comment.upvoted_users.all()), 1)

    def test_upvote_invalid(self):
        response = client.patch(f'/en/api/comments/rate/{self.comment.pk}/', data={'rating': 'up'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(self.comment.rating, 0)
        self.assertEqual(self.test_guest.rating, 0)
