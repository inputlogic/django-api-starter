from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .serializers import UserChangePasswordSerializer


class UserChangePasswordView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserChangePasswordSerializer

    def get_object(self):
        return self.request.user
