from django.contrib.auth import get_user_model
from rest_framework import serializers


class UserMyProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'email')
        read_only_fields = ('id', 'email')
