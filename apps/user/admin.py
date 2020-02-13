from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

User = get_user_model()
USERNAME_FIELD = User.USERNAME_FIELD
REQUIRED_FIELDS = (USERNAME_FIELD,) + tuple(User.REQUIRED_FIELDS)


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    list_display = ('email', 'is_active')
    fieldsets = (
        (None, {'fields': REQUIRED_FIELDS + (
            'is_active',
            'is_staff',
            'is_superuser',
            'date_joined',
            'last_login',
        )}),
        ('Password', {'fields': (
            'password',
        )}),
    )
    add_fieldsets = (
        (None, {'fields': REQUIRED_FIELDS + (
            'password1',
            'password2',
        )}),
    )
    readonly_fields = (
        'date_joined',
        'last_login'
    )
    search_fields = (USERNAME_FIELD,)
    ordering = (USERNAME_FIELD,)
    list_filter = ()
