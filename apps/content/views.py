from rest_framework import viewsets
from .serializers import ContentSerializer
from .models import Content
from libs.permissions import IsAdminUserOrReadOnly


class ContentViewSet(viewsets.ModelViewSet):
    queryset = Content.objects.all()
    serializer_class = ContentSerializer
    permission_classes = (IsAdminUserOrReadOnly,)
