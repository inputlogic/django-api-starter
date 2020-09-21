from rest_framework import generics

from .models import File
from .serializers import CreateSignedFileSerializer, FileSerializer


class CreateSignedFile(generics.CreateAPIView):
    serializer_class = CreateSignedFileSerializer


class FileDetail(generics.RetrieveDestroyAPIView):
    queryset = File.objects
    serializer_class = FileSerializer
