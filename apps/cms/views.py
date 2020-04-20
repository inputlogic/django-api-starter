from rest_framework import generics, permissions

from .models.work import Work
from .models.page import Page
from .serializers.work import WorkSerializer
from .serializers.page import PageSerializer


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

