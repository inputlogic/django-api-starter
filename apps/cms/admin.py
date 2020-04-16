from django.contrib import admin

from adminsortable.admin import SortableAdmin, SortableTabularInline
from mptt.admin import DraggableMPTTAdmin

from .models import Page, Section


class SectionInline(SortableTabularInline):
    model = Section
    extra = 0


@admin.register(Page)
class PageAdmin(SortableAdmin, DraggableMPTTAdmin):
    list_display = ('tree_actions', 'indented_title', 'slug',)
    list_display_links = ('indented_title',)
    readonly_fields = ('slug',)
    inlines = (SectionInline,)
