from rest_framework import serializers

from .tag import TagSerializer
from ..models.post import Post


class PostSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)

    class Meta:
        model = Post
        fields = (
            'id',
            'title',
            'slug',
            'published',
            'published_on',
            'feature_image',
            'feature_color',
            'body',
            'tags',
            'updated_at',
        )
