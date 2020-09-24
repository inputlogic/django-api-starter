from django.contrib import admin
from .models import File


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_filter = ('is_verified', 'is_private', 'mime_type')
    list_display = ('filename', 'is_verified', 'is_private', 'mime_type', 'created_at')

    def filename(self, obj):
        return str(obj)
