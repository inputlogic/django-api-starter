from rest_framework import serializers

from ..models.profiles import Profile


class PublicProfileDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('id', 'about',)


class ProfileDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('id', 'about',)
