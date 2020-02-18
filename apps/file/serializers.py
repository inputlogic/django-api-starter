from rest_framework import serializers

from .models import File
from .libs import get_upload_url


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ('link', 'id')


class CreateSignedFileSerializer(serializers.Serializer):
    file_name = serializers.CharField(write_only=True)
    acl = serializers.CharField(write_only=True, required=False)
    file_id = serializers.PrimaryKeyRelatedField(read_only=True)
    url = serializers.URLField(read_only=True)
    content_type = serializers.CharField(read_only=True)

    def create(self, validated_data):
        data = get_upload_url(**validated_data)
        newfile = File.objects.create(
            user=self.context['request'].user,
            link=data['url'].split('?')[0],  # Only insert actual path, not the signature params
            is_private=validated_data.get('acl') == 'private',
            mime_type=data['content_type']
        )
        data['file_id'] = newfile.id
        return data
