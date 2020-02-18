from rest_framework import serializers

from .models import Firebase


class FirebaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Firebase
        fields = (
            'user',
            'registration_id',
            'created_at',
            'updated_at',
        )
        read_only_fields = ('user', 'created_at', 'updated_at',)

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        obj, _ = Firebase.objects.get_or_create(**validated_data)
        return obj
