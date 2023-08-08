from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password as django_validate_password
from django.contrib.auth import get_user_model


class UserChangePasswordSerializer(serializers.ModelSerializer):
    new_password = serializers.CharField(write_only=True)

    class Meta:
        model = get_user_model()
        fields = ('password', 'new_password')
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise ValidationError('Invalid current password.')
        return value

    def validate(self, data):
        if data['password'] == data['new_password']:
            raise ValidationError(
                "New password should be different from the current password.")
        django_validate_password(
            data['new_password'], self.context['request'].user)
        return data

    def create(self, validated_data):
        user = self.context['request'].user
        user.set_password(validated_data['new_password'])
        user.save()
        return user
