from django.contrib import admin

from .models import Content


@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = ('id', 'page', 'identifier', 'value')
    search_fields = ('page', 'identifier', 'value')
