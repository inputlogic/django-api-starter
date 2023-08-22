from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from rest_framework import serializers

from apps.user import mail


class PublicForgotPasswordStep1Serializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)

    def create(self, validated_data):
        email = validated_data['email'].lower()
        try:
            user = get_user_model().objects.get(email=email)
        except get_user_model().DoesNotExist:
            return {}

        reset_token = default_token_generator.make_token(user)
        mail.send_forgot_password_email(user, reset_token=reset_token)

        return {}
