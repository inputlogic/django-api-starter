from rest_framework import serializers


class FacebookCodeExchangeSerializer(serializers.Serializer):
    code = serializers.CharField(allow_blank=False, required=True)


class FacebookTokenExchangeSerializer(serializers.Serializer):
    facebook_user_token = serializers.CharField(allow_blank=False, required=True)
