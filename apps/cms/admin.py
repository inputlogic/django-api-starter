from django.contrib import admin
from django.db import models

from adminsortable2.admin import SortableInlineAdminMixin
from mptt.admin import DraggableMPTTAdmin

from .models import Tag, Page, Section, Work, Slide
from .widgets import AdminImageWidget


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


class SlideInline(SortableInlineAdminMixin, admin.TabularInline):
    model = Slide
    extra = 0
    formfield_overrides = {
        models.ImageField: {'widget': AdminImageWidget},
    }


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
        ('Intro', {
            'fields': (('intro_image', 'intro_body',),),
        }),
    )
    formfield_overrides = {
        models.ImageField: {'widget': AdminImageWidget},
    }
