from rest_framework import serializers

from .models import Work, Slide, Page, Section


meta_fields = ('meta_title', 'meta_description', 'og_title', 'og_type', 'og_description')


class MetadataBaseSerializer(serializers.ModelSerializer):
    meta_title = serializers.SerializerMethodField()
    og_title = serializers.SerializerMethodField()
    meta_description = serializers.SerializerMethodField()
    og_description = serializers.SerializerMethodField()

    def get_meta_title(self, obj):
        return obj.meta_title or obj.og_title or obj.title

    def get_og_title(self, obj):
        return obj.og_title or obj.meta_title or obj.title

    def get_meta_description(self, obj):
        return obj.meta_description or obj.og_description or ''
    
    def get_og_description(self, obj):
        return obj.og_description or obj.meta_description or ''


# Work Posts


class SlideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slide
        fields = (
            'id',
            'title',
            'image',
            'body',
            'sort_order',
        )


class WorkSerializer(serializers.ModelSerializer):
    slides = serializers.SerializerMethodField()

    class Meta:
        model = Work
        fields = (
            'id',
            'title',
            'slug',
            'headline',
            'intro_image',
            'intro_body',
            'slides',
            'created_at',
            'updated_at',
        )

    def get_slides(self, work):
        slides = Slide.objects.filter(work=work)
        serializer_context = {
            'request': self.context.get('request')
        }
        serializer = SlideSerializer(
            slides,
            context=serializer_context,
            many=True,
            read_only=True,
        )
        return serializer.data


# Pages


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

