from django.contrib import admin
from django.db import models

from adminsortable2.admin import SortableInlineAdminMixin
from mptt.admin import DraggableMPTTAdmin

from .models.page import Page, Section
from .models.post import Post
from .models.tag import Tag
from .widgets import AdminImageWidget


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug',)
    actions = None
    list_per_page = 25
    fields = ('title',)
    search_fields = ('title',)


class SectionInline(SortableInlineAdminMixin, admin.TabularInline):
    model = Section
    extra = 0
    classes = ['layout_sectioned',]


@admin.register(Page)
class PageAdmin(DraggableMPTTAdmin):
    list_display = ('tree_actions', 'indented_title', 'slug',)
    list_display_links = ('indented_title',)
    readonly_fields = ('slug',)
    inlines = (SectionInline,)
    fieldsets = (
        (None, {
            'fields': (('title', 'slug'), 'sub_title', 'layout',)
        }),
        ('Metadata', {
            'classes': ('collapse', 'open'),
            'fields': (
                'meta_title',
                'meta_description',
                'og_title',
                'og_description',
                'og_type',
            ),
        }),
        ('Content', {
            'classes': ('layout_simple',),
            'fields': ('sidebar', 'body',),
        }),
    )

    class Media:
        js = ('jQuery.js', 'cms/js/page.js',)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug',)
    list_display_links = ('title',)
    readonly_fields = ('slug',)
    autocomplete_fields = ('tags',)
    fieldsets = (
        (None, {
            'fields': (('title', 'slug'), 'tags', 'published_on', 'published',)
        }),
        ('Feature', {
            'classes': ('collapse',),
            'fields': (('feature_image', 'feature_color',),),
        }),
        ('Content', {
            'fields': ('body',)
        })
    )
    formfield_overrides = {
        models.ImageField: {'widget': AdminImageWidget},
    }
