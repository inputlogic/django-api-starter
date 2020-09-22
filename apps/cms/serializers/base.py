from rest_framework import serializers


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
