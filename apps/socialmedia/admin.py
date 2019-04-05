from django.contrib import admin

from .models import SocialMedia


@admin.register(SocialMedia)
class SocailMediaAdmin(admin.ModelAdmin):
    list_display = ('user', 'source', 'identifier')
    fieldsets = (
        (None, {'fields': ('user', 'source', 'identifier')}),
    )
    readonly_fields = (
        'user', 'source', 'identifier'
    )
    search_fields = ('user', 'source', 'identifier')
    list_filter = ()
    ordering = ('user',)
    filter_horizontal = ()
    filter_vertical = ()
    actions = None

    def has_add_permission(self, request, obj=None):
        return False
