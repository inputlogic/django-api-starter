from rest_framework import serializers

from .models import Work, Slide, Page, Section


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


class PageSerializer(serializers.ModelSerializer):
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
        )

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

