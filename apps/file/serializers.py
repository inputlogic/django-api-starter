from rest_framework import serializers

from .models import File
from .libs import signed_url


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ('link', 'id')


class CreateSignedFileSerializer(serializers.Serializer):
    file_name = serializers.CharField(write_only=True)
    is_private = serializers.BooleanField(write_only=True, required=False)
    s3Data = serializers.JSONField(read_only=True)
    url = serializers.URLField(read_only=True)
    fileId = serializers.IntegerField(read_only=True)

    def create(self, validated_data):
        is_private = validated_data.get('is_private', False)
        permissions = 'public-read' if not is_private else 'bucket-owner-read'
        signed = signed_url(validated_data['file_name'], permissions=permissions)
        the_file = File.objects.create(
            link=signed['url'],
            user=self.context['request'].user,
            is_private=is_private,
            mime_type=signed['mime_type'],
        )
        return {
            's3Data': signed['data'],
            'url': signed['url'],
            'fileId': the_file.id
        }
