from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from rest_framework import serializers
from rest_framework.exceptions import ParseError


class PublicForgotPasswordStep2Serializer(serializers.Serializer):
    token = serializers.CharField(write_only=True)
    user_id = serializers.IntegerField(write_only=True)
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        token = validated_data['token']
        user_id = validated_data['user_id']
        password = validated_data['password']

        user = get_user_model().objects.get(id=user_id)
        if not default_token_generator.check_token(user, token):
            raise ParseError(detail='Invalid token')

        user.set_password(password)
        user.save()
        return {}
