from django.test import TestCase
from .views import *


class PostModelTest(TestCase):
    post_id = None

    # @classmethod
    # def setUpTestData(cls) -> None:
    #     post = Post.objects.create(name='TestPost',
    #                                description='Lorem ipsum',
    #                                text='Lorem ipsum dolor sit amet, consectetur adipiscing elit',
    #                                user=Guest.objects.get(name='admin'))
    #     cls.post_id = post.id

    def test_create(self):
        pass

    def test_retrieve(self):
        pass

    def test_list(self):
        pass

    def test_update(self):
        pass

    def test_partial_update(self):
        pass

    def test_destroy(self):
        pass


class CommentModelTest(TestCase):

    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def test_create(self):
        pass

    def test_retrieve(self):
        pass

    def test_list(self):
        pass

    def test_update(self):
        pass

    def test_partial_update(self):
        pass

    def test_destroy(self):
        pass
