from rest_framework import serializers


class FacebookCodeExchangeSerializer(serializers.Serializer):
    code = serializers.CharField(required=True)
