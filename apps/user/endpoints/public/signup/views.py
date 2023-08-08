from django.contrib.auth import get_user_model
from rest_framework import generics, permissions

from apps.user import mail
from .serializers import PublicSignupSerializer


class PublicSignupView(generics.CreateAPIView):
    serializer_class = PublicSignupSerializer
    permission_classes = (permissions.AllowAny,)

    def perform_create(self, serializer):
        data = serializer.save()
        user = get_user_model().objects.get(id=data['user_id'])
        mail.send_welcome_email(user)
