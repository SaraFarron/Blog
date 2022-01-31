from rest_framework.fields import CharField, IntegerField, ChoiceField
from rest_framework.serializers import ModelSerializer, StringRelatedField, SlugRelatedField

from BlogApp.models import Post, Comment, Guest


class UserSerializer(ModelSerializer):
    rating = IntegerField(read_only=True)

    class Meta:
        model = Guest
        fields = ('name', 'email', 'phone', 'skype', 'is_banned', 'is_muted', 'last_ban_date', 'is_moderator', 'rating')


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
    user = SlugRelatedField(
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


class RatePostSerializer(ModelSerializer):
    rating = ChoiceField(choices=['upvote', 'downvote'])

    class Meta:
        model = Post
        fields = ['rating']


class RateCommentSerializer(ModelSerializer):
    rating = ChoiceField(choices=['upvote', 'downvote'])

    class Meta:
        model = Comment
        fields = ['rating']


# class SavePostSerializer(ModelSerializer):
#     rating = ChoiceField(choices=['upvote', 'downvote'])
#
#     class Meta:
#         model = Post
#         fields = ['rating']
#
#
# class SaveCommentSerializer(ModelSerializer):
#     rating = ChoiceField(choices=['upvote', 'downvote'])
#
#     class Meta:
#         model = Comment
#         fields = ['rating']
