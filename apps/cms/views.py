from datetime import datetime

from rest_framework import generics, permissions

from .models.post import Post
from .models.page import Page
from .serializers.post import PostSerializer
from .serializers.page import PageSerializer

from .filters import PostFilters


class PostDetail(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (permissions.AllowAny,)


class PostList(generics.ListAPIView):
    queryset = Post.objects.filter(published=True)
    serializer_class = PostSerializer
    permission_classes = (permissions.AllowAny,)
    filter_class = PostFilters

    def get_queryset(self):
        """
        Don't return Posts scheduled to be published in the future.
        """
        return self.queryset.filter(published_on__lte=datetime.today())


class PageDetail(generics.RetrieveAPIView):
    queryset = Page.objects.all()
    serializer_class = PageSerializer
    permission_classes = (permissions.AllowAny,)


class PageList(generics.ListAPIView):
    queryset = Page.objects.all()
    serializer_class = PageSerializer
    permission_classes = (permissions.AllowAny,)
