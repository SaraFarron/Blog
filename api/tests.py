import json
from django.test import TestCase
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from rest_framework import status

from .serializers import *

token = Token.objects.get(user__username='admin')
client = APIClient()
client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)


class PostViewSetTest(TestCase):

    def setUp(self) -> None:
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

    def test_list(self):
        response = client.get('/en/api/posts/')
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve(self):
        response = client.get('/en/api/posts/', kwargs={'pk': self.first_post.pk})
        posts = Post.objects.get(pk=self.first_post.pk)
        serializer = PostSerializer(posts)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_valid(self):
        response = client.post(
            '/en/api/posts/',
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid(self):
        response = client.post(
            '/en/api/posts/',
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_valid(self):
        response = client.put(
            '/en/api/posts/', kwargs={'pk': self.second_post.pk},
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_update_invalid(self):
        response = client.post(
            '/en/api/posts/', kwargs={'pk': self.second_post.pk},
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_valid(self):
        response = client.delete(
            '/en/api/posts/', kwargs={'pk': self.third_post.pk})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_invalid(self):
        response = client.delete(
            '/en/api/posts/', kwargs={'pk': 99})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


