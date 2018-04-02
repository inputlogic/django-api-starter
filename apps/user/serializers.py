from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.contrib.auth.tokens import default_token_generator


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'email', 'password')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = get_user_model()(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, obj, validated_data):
        password = validated_data.pop('password', None)
        if password:
            obj.set_password(password)
        return super().update(obj, validated_data)
