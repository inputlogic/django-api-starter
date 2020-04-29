from django_filters import rest_framework as filters

from .models.post import Post


class NumberInFilter(filters.BaseInFilter, filters.NumberFilter):
    pass


class PostFilters(filters.FilterSet):
    published_after = filters.IsoDateTimeFilter(field_name="published_on", lookup_expr="gte")
    published_before = filters.IsoDateTimeFilter(field_name="published_on", lookup_expr="lte")
    tagged = NumberInFilter(field_name='tags__id', lookup_expr='in')

    class Meta:
        model = Post
        fields = ('published_after', 'published_before', 'tagged')

