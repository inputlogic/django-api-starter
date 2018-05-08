from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'is_active')
    fieldsets = (
        (None, {'fields': ('email', 'company', 'is_active')}),
        ('Password', {'fields': ('password',)}),
    )
    search_fields = ()
    list_filter = ()
    ordering = ('email',)
    filter_horizontal = ()
    filter_vertical = ()
    actions = None


admin.site.register(get_user_model(), UserAdmin)
admin.site.unregister(Group)
