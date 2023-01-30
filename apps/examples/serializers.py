from rest_framework import serializers


class HTMLArraySerializer(serializers.Serializer):
    name = serializers.CharField()
    hours_open = serializers.IntegerField()
    foods = serializers.ListField()
