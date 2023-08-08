from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .serializers import UserMyProfileSerializer


class UserMyProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserMyProfileSerializer

    def get_object(self):
        return self.request.user
