from rest_framework.serializers import ModelSerializer

from .models import Post


class PostSerializer(ModelSerializer):
    class Meta:
        fields = ('id', 'text', 'author', 'image', 'pub_date')
        model = Post
