from rest_framework import generics

from .serializers import CreateSignedFileSerializer


class CreateSignedFile(generics.CreateAPIView):
    serializer_class = CreateSignedFileSerializer
