from rest_framework import generics, permissions

from .models import Work, Page
from .serializers import WorkSerializer, PageSerializer


class WorkDetail(generics.RetrieveAPIView):
    queryset = Work.objects.all()
    serializer_class = WorkSerializer
    permission_classes = (permissions.AllowAny,)


class WorkList(generics.ListAPIView):
    queryset = Work.objects.all()
    serializer_class = WorkSerializer
    permission_classes = (permissions.AllowAny,)


class PageDetail(generics.RetrieveAPIView):
    queryset = Page.objects.all()
    serializer_class = PageSerializer
    permission_classes = (permissions.AllowAny,)


class PageList(generics.ListAPIView):
    queryset = Page.objects.all()
    serializer_class = PageSerializer
    permission_classes = (permissions.AllowAny,)

