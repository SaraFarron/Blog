from rest_framework.serializers import ModelSerializer, StringRelatedField
from BlogApp.models import Post, Comment


class PostSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'


class CommentSerializer(ModelSerializer):
    post = StringRelatedField()

    class Meta:
        model = Comment
        fields = '__all__'
        depth = 3
