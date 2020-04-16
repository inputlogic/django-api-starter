from django.contrib import admin

from adminsortable2.admin import SortableInlineAdminMixin
from mptt.admin import DraggableMPTTAdmin

from .models import Tag, Page, Section, Work, Slide


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('title',)
    actions = None
    list_per_page = 25
    fields = ('title',)
    search_fields = ('title',)


class SectionInline(SortableInlineAdminMixin, admin.TabularInline):
    model = Section
    extra = 0


@admin.register(Page)
class PageAdmin(DraggableMPTTAdmin):
    list_display = ('tree_actions', 'indented_title', 'slug',)
    list_display_links = ('indented_title',)
    readonly_fields = ('slug',)
    inlines = (SectionInline,)


class SlideInline(SortableInlineAdminMixin, admin.TabularInline):
    model = Slide
    extra = 0


@admin.register(Work)
class WorkAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug',)
    list_display_links = ('title',)
    readonly_fields = ('slug',)
    autocomplete_fields = ('tags',)
    inlines = (SlideInline,)
    fieldsets = (
        (None, {
            'fields': (('title', 'slug'), 'headline', 'tags')
        }),
        ('Content', {
            'fields': ('intro_image', 'intro_body', 'body',),
        }),
    )
