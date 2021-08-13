from rest_framework.serializers import ModelSerializer, StringRelatedField, SlugRelatedField
from BlogApp.models import Post, Comment


class PostSerializer(ModelSerializer):
    user = StringRelatedField()

    class Meta:
        model = Post
        fields = '__all__'


class CommentSerializer(ModelSerializer):
    post = StringRelatedField()
    author = SlugRelatedField(
        read_only=True,
        slug_field='name'
    )

    class Meta:
        model = Comment
        fields = '__all__'
        depth = 3
