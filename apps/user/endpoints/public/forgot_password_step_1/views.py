from rest_framework import generics, permissions

from .serializers import PublicForgotPasswordStep1Serializer


class PublicForgotPasswordStep1View(generics.CreateAPIView):
    serializer_class = PublicForgotPasswordStep1Serializer
    permission_classes = (permissions.AllowAny,)
