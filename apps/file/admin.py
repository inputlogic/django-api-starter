from django.contrib import admin
from .models import File


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ('link', 'is_private', 'user', 'mime_type')
