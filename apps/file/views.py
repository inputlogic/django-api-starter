from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import permissions, generics

from .libs import signed_url
from .models import File
from .serializers import FileSerializer, CreateSignedFileSerializer


class CreateSignedFile(generics.CreateAPIView):
    serializer_class = CreateSignedFileSerializer


class FileDetail(generics.RetrieveDestroyAPIView):
    queryset = File.objects
    serializer_class = FileSerializer
