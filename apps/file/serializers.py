from rest_framework import serializers

from .models import File
from .libs import signed_url


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ('link', 'id', 'created_at',)


class CreateSignedFileSerializer(serializers.Serializer):
    file_name = serializers.CharField(write_only=True)
    acl = serializers.CharField(write_only=True, required=False)
    content_type = serializers.CharField(write_only=True, required=False)

    file_id = serializers.IntegerField(read_only=True)
    url = serializers.URLField(read_only=True)
    s3_data = serializers.JSONField(read_only=True)

    def create(self, validated_data):
        file_name = validated_data['file_name'].replace(' ', '_')

        signed = signed_url(
            file_name=file_name,
            content_type=validated_data.get('content_type', None)
        )

        file_instance = File.objects.create(
            link=signed['url'],
            user=self.context['request'].user
        )

        return {
            's3_data': signed['data'],
            'url': signed['url'],
            'file_id': file_instance.id
        }
