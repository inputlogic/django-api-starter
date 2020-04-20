from rest_framework import serializers

from ..models.work import Work, Slide


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
