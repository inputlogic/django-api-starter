import operator
import urllib

from datetime import datetime

from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector

from rest_framework import generics, permissions, status
from rest_framework.response import Response

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
    search_fields = ['title', 'body']

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
    search_fields = ['title', 'sub_title', 'body']


class Search(generics.GenericAPIView):
    """
    A 'site-wide' search.

    Adapt the `get` method to include more model types.
    """
    permission_classes = (permissions.AllowAny,)

    def get(self, request, *args, **kwargs):
        keywords = request.query_params.get('keywords', '')
        keywords = urllib.parse.unquote(keywords)
        ctx = {'request': request}
        query = SearchQuery(keywords)

        # Posts

        post_vector = (
            SearchVector('title', weight='A') +
            SearchVector('body', weight='C')
        )

        posts = (
            Post
            .objects
            .annotate(rank=SearchRank(post_vector, query))
            .filter(rank__gte=0.1)
            .distinct('id')
        )

        posts = sorted(posts, key=operator.attrgetter('rank'), reverse=True)
        posts_serializer = PostSerializer(posts, context=ctx, many=True)

        # Pages

        page_vector = (
            SearchVector('title', weight='A') +
            SearchVector('sub_title', weight='B') +
            SearchVector('body', weight='C')
        )

        pages = (
            Page
            .objects
            .annotate(rank=SearchRank(page_vector, query))
            .filter(rank__gte=0.1)
        )

        pages = sorted(pages, key=operator.attrgetter('rank'), reverse=True)
        pages_serializer = PageSerializer(pages, context=ctx, many=True)

        # Combine into Response

        results = {
            'posts': posts_serializer.data,
            'pages': pages_serializer.data,
        }

        return Response(results, status.HTTP_200_OK)
