from django.contrib import admin

from adminsortable2.admin import SortableInlineAdminMixin
from mptt.admin import DraggableMPTTAdmin

from .models import Page, Section


class SectionInline(SortableInlineAdminMixin, admin.TabularInline):
    model = Section
    extra = 0


@admin.register(Page)
class PageAdmin(DraggableMPTTAdmin):
    list_display = ('tree_actions', 'indented_title', 'slug',)
    list_display_links = ('indented_title',)
    readonly_fields = ('slug',)
    inlines = (SectionInline,)
