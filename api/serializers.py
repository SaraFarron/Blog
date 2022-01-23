from rest_framework.fields import CharField, IntegerField
from rest_framework.serializers import ModelSerializer, StringRelatedField, SlugRelatedField

from BlogApp.models import Post, Comment, Guest


class UserSerializer(ModelSerializer):
    class Meta:
        model = Guest
        fields = ('name', 'email', 'phone', 'skype', 'is_banned', 'is_muted', 'last_ban_date', 'is_moderator')


class PostSerializer(ModelSerializer):
    user = StringRelatedField()
    rating = IntegerField(read_only=True)
    number_of_comments = IntegerField(read_only=True)
    upvoted_users = StringRelatedField(read_only=True, many=True)
    downvoted_users = StringRelatedField(read_only=True, many=True)
    saved_by = StringRelatedField(read_only=True, many=True)

    class Meta:
        model = Post
        fields = '__all__'


class CommentSerializer(ModelSerializer):
    id = IntegerField(read_only=True)
    post = CharField(required=True)
    author = SlugRelatedField(
        read_only=True,
        slug_field='name'
    )
    parent_comment = IntegerField(required=False)
    rating = IntegerField(read_only=True)
    upvoted_users = StringRelatedField(read_only=True, many=True)
    downvoted_users = StringRelatedField(read_only=True, many=True)
    saved_by = StringRelatedField(read_only=True, many=True)
    replies = StringRelatedField(read_only=True, many=True)

    class Meta:
        model = Comment
        fields = '__all__'
        depth = 1
