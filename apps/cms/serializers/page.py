from rest_framework import serializers

from .base import meta_fields, MetadataBaseSerializer
from ..models.page import Page, Section


class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = (
            'id',
            'title',
            'image',
            'body',
            'sort_order',
        )


class PageSerializer(MetadataBaseSerializer):
    sections = serializers.SerializerMethodField()

    class Meta:
        model = Page
        fields = (
            'id',
            'tree_id',
            'title',
            'slug',
            'sub_title',
            'layout',
            'body',
            'sidebar',
            'sections',
            'parent',
            'created_at',
            'updated_at',
        ) + meta_fields

    def get_sections(self, page):
        sections = Section.objects.filter(page=page)
        serializer_context = {
            'request': self.context.get('request')
        }
        serializer = SectionSerializer(
            sections,
            context=serializer_context,
            many=True,
            read_only=True,
        )
        return serializer.data

    def get_meta_description(self, obj):
        return obj.meta_description or obj.og_description or obj.sub_title or ''

    def get_og_description(self, obj):
        return obj.og_description or obj.meta_description or obj.sub_title or ''
