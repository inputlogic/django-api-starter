from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ValidationError


class UserChangeEmailSerializer(serializers.ModelSerializer):
    new_email = serializers.CharField(write_only=True)

    class Meta:
        model = get_user_model()
        fields = ('password', 'new_email')
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise ValidationError('Invalid password.')
        return value

    def create(self, validated_data):
        user = self.context['request'].user
        user.email = validated_data['new_email']
        user.save()
        return user
