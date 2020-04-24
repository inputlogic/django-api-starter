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
            'feature_image',
            'feature_color',
            'tags',
            'created_at',
            'updated_at',
        )
