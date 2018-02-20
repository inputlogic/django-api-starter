from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.contrib.auth.tokens import default_token_generator

from .profile import PublicProfileDetailSerializer, ProfileDetailSerializer
from ..models.profiles import Profile

# from . import emails


class UserCreateSerializer(serializers.ModelSerializer):
    profile = ProfileDetailSerializer(required=False)

    class Meta:
        model = get_user_model()
        fields = ('id', 'first_name', 'last_name', 'email', 'password', 'profile')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        profile = validated_data.pop('profile') if 'profile' in validated_data else {}
        user = get_user_model()(**validated_data)
        user.set_password(password)
        user.save()
        Profile.objects.create(user=user, **profile)
        # emails.new_account(user.email)
        return user


class PublicUserDetailSerializer(serializers.ModelSerializer):
    profile = PublicProfileDetailSerializer(required=False)

    class Meta:
        model = get_user_model()
        fields = ('id', 'first_name', 'last_name')


class UserDetailSerializer(serializers.ModelSerializer):
    profile = ProfileDetailSerializer(required=False)

    class Meta:
        model = get_user_model()
        fields = ('id', 'first_name', 'last_name', 'email', 'profile')

    def update(self, user, validated_data):
        profile = validated_data.pop('profile') if 'profile' in validated_data else {}
        super().update(user, validated_data)
        if hasattr(user, 'profile'):
            ProfileDetailSerializer().update(user.profile, profile)
        else:
            Profile.objects.create(user=user, **profile)
        return user
