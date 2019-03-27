from django.conf import settings
from rest_framework import generics, serializers
from rest_framework.permissions import BasePermission
from rest_framework.exceptions import ValidationError
from .models import Template


class MailAuth(BasePermission):
    def has_permission(self, request, view):
        given_api_key = request.META['HTTP_API_KEY']
        actual_api_key = settings.MAIL_SECRET_KEY
        return given_api_key == actual_api_key


class TemplateSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    subject = serializers.CharField(allow_blank=True)
    body = serializers.CharField(allow_blank=True)

    class Meta:
        model = Template
        fields = ('id', 'name', 'subject', 'body', 'data_example')

    def create(self, validated_data):
        try:
            template = Template.objects.get(name=validated_data['name'])
            if not template.same_data_structure(validated_data['data_example']):
                raise ValidationError({
                    'example_data': 'A template with this name and a different data structure already exists.'
                })
            template.data_example = validated_data['data_example']
            template.save()
            return template
        except Template.DoesNotExist:
            return super().create(validated_data)


class TemplateCreate(generics.CreateAPIView):
    queryset = Template.objects.all()
    serializer_class = TemplateSerializer
    permission_classes = (MailAuth,)
