from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin

from .models import Page


@admin.register(Page)
class PageAdmin(DraggableMPTTAdmin):
    list_display = ('tree_actions', 'indented_title', 'slug',)
    list_display_links = ('indented_title',)
    readonly_fields = ('slug',)
