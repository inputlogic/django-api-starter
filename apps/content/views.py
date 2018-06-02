from rest_framework import viewsets, permissions
from .serializers import ContentSerializer
from .models import Content


class ContentViewSet(viewsets.ModelViewSet):
    queryset = Content.objects.all()
    serializer_class = ContentSerializer
    permission_classes = (permissions.AllowAny,)
