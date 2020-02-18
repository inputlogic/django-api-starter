from rest_framework import generics, permissions

from libs.permissions import IsOwnerOrReadOnly

from .models import Firebase
from .serializers import FirebaseSerializer


class FirebaseListCreate(generics.ListCreateAPIView):
    serializer_class = FirebaseSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Firebase.objects.filter(user=self.request.user)


class FirebaseDestroy(generics.DestroyAPIView):
    serializer_class = FirebaseSerializer
    permission_classes = (IsOwnerOrReadOnly,)
    lookup_field = 'registration_id'

    def get_queryset(self):
        return Firebase.objects.filter(user=self.request.user)
