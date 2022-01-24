import json
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User

from .serializers import *

# token = Token.objects.get(user__username='admin')
client = APIClient()
# client.force_authenticate(user=token.user, token=token)
# client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
# print(token.user)


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
        self.assertEqual(json.dumps(response.data), serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve(self):
        response = client.get(f'/en/api/posts/{self.first_post.pk}/')
        posts = Post.objects.get(pk=self.first_post.pk)
        serializer = PostSerializer(posts)
        self.assertEqual(json.dumps(response.data), serializer.data)
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
