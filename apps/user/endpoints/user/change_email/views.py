from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .serializers import UserChangeEmailSerializer


class UserChangeEmailView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserChangeEmailSerializer

    def get_object(self):
        return self.request.user
