from rest_framework import generics, permissions
from .serializers import PublicForgotPasswordStep2Serializer


class PublicForgotPasswordStep2View(generics.CreateAPIView):
    serializer_class = PublicForgotPasswordStep2Serializer
    permission_classes = (permissions.AllowAny,)
