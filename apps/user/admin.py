from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib import admin
from authtools.admin import UserAdmin

from .models import SocialMedia


class UserAdmin(UserAdmin):
    list_display = ('email', 'is_active')
    fieldsets = (
        (None, {'fields': ('email', 'is_active')}),
        ('Password', {'fields': ('password',)}),
    )
    search_fields = ()
    list_filter = ()
    ordering = ('email',)
    filter_horizontal = ()
    filter_vertical = ()
    actions = None


@admin.register(SocialMedia)
class SocailMediaAdmin(admin.ModelAdmin):
    list_display = ('user', 'source', 'identifier')
    fieldsets = (
        (None, {'fields': ('user', 'source', 'identifier')}),
    )
    search_fields = ('user', 'source', 'identifier')
    list_filter = ()
    ordering = ('user',)
    filter_horizontal = ()
    filter_vertical = ()
    actions = None


admin.site.register(get_user_model(), UserAdmin)
admin.site.unregister(Group)
