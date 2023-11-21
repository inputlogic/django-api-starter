from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import File
from .libs import signed_url


class FileSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(
        queryset=get_user_model().objects.all(),
        default=serializers.CurrentUserDefault()
    )
    upload = serializers.FileField(write_only=True)
    url = serializers.FileField(read_only=True, source='upload')
    is_verified = serializers.BooleanField(default=True)

    class Meta:
        model = File
        extra_kwargs = {
            'mime_type': {'read_only': True},
            'is_private': {'read_only': True},
            'is_resized': {'read_only': True},
        }
        fields = (
            'id',
            'owner',
            'upload',
            'url',
            'mime_type',
            'is_private',
            'is_resized',
            'is_verified',
            'created_at',
        )


class CreateSignedFileSerializer(serializers.Serializer):
    file_name = serializers.CharField(write_only=True)
    acl = serializers.CharField(write_only=True, required=False)
    content_type = serializers.CharField(write_only=True, required=False)

    file_id = serializers.IntegerField(read_only=True)
    url = serializers.URLField(read_only=True)
    presigned_url = serializers.URLField(read_only=True)
    content_type = serializers.CharField(read_only=True)

    def create(self, validated_data):
        file_name = validated_data['file_name'].replace(' ', '_')

        signed = signed_url(
            file_name=file_name,
            content_type=validated_data.get('content_type', None)
        )

        file_obj = File.objects.create(
            owner=self.context['request'].user,
            mime_type=signed['content_type']
        )

        file_obj.upload.name = signed['url'].split('/')[-1]
        file_obj.save()

        return {
            **signed,
            'file_id': file_obj.id
        }
