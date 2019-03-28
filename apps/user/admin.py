from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib import admin
from authtools.admin import UserAdmin


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


admin.site.register(get_user_model(), UserAdmin)
admin.site.unregister(Group)
