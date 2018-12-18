from django.contrib import admin
from .models import File


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_filter = ('verified', 'is_private', 'mime_type')
    list_display = ('filename', 'verified', 'is_private', 'mime_type', 'created_at')

    def filename(self, obj):
        return str(obj)
