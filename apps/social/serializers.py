from rest_framework import serializers


class CodeExchangeSerializer(serializers.Serializer):
    code = serializers.CharField(allow_blank=False, required=True)


class FacebookTokenExchangeSerializer(serializers.Serializer):
    facebook_user_token = serializers.CharField(allow_blank=False, required=True)


class GoogleTokenExchangeSerializer(serializers.Serializer):
    google_user_token = serializers.CharField(allow_blank=False, required=True)
