from rest_framework import generics
from rest_framework.parsers import FormParser, MultiPartParser

from .models import File
from .serializers import CreateSignedFileSerializer, FileSerializer


class CreateSignedFile(generics.CreateAPIView):
    """ Create signed file.

    This creates a file instance and generates a signed URL that the
    client can upload to directly.
    """
    serializer_class = CreateSignedFileSerializer


class UploadFile(generics.CreateAPIView):
    """ Upload file.

    This handles uploading a file on the server, rather than returning
    a signed URL for AWS S3 or the like. Though, with django-storages,
    the file may very well likely end up on S3 anyway.
    """
    parser_classes = [FormParser, MultiPartParser]
    serializer_class = FileSerializer


class FileDetail(generics.RetrieveDestroyAPIView):
    queryset = File.objects
    serializer_class = FileSerializer
