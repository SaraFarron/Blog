from rest_framework.fields import CharField
from rest_framework.serializers import (ModelSerializer, StringRelatedField, SlugRelatedField, )
from BlogApp.models import Post, Comment, Guest


class PostSerializer(ModelSerializer):
    user = StringRelatedField()

    class Meta:
        model = Post
        fields = '__all__'


class CommentSerializer(ModelSerializer):
    post = CharField(required=True)
    author = SlugRelatedField(
        read_only=True,
        slug_field='name'
    )

    class Meta:
        model = Comment
        fields = '__all__'
        depth = 1


class UserSerializer(ModelSerializer):
    class Meta:
        model = Guest
        fields = ('name', 'email', 'phone', 'skype', 'is_banned', 'is_muted', 'last_ban_date', 'is_moderator')
