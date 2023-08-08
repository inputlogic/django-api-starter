from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework import serializers


class PublicSignupSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)
    token = serializers.CharField(read_only=True)

    class Meta:
        model = get_user_model()
        fields = ('email', 'password', 'user_id', 'token')
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'write_only': True},
        }

    def validate_email(self, value):
        norm_email = value.lower()
        if get_user_model().objects.filter(email=norm_email).exists():
            raise serializers.ValidationError(
                "user with this email address already exists.")
        return norm_email

    def create(self, validated_data):
        user = get_user_model().objects.create_user(**validated_data)
        token = Token.objects.create(user=user)
        return {
            'token': token.key,
            'user_id': user.id
        }
