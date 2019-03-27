from django.contrib import admin
from django.utils.html import format_html

from .models import Mail
from .libs.pretty_json import pretty_json


@admin.register(Mail)
class MailAdmin(admin.ModelAdmin):
    list_display = ('subject', 'email', 'name', 'status', 'created_at')
    fields = ('name', 'user', 'email_subject', 'email_body', 'email_data', 'status')
    readonly_fields = fields

    def email_subject(self, obj):
        return format_html('{0}', obj.subject)

    def email_body(self, obj):
        return format_html(
            '<iframe srcdoc="{0}" style="width: 100%; height: 800px; border: 1px solid #f0f0f0" ></iframe>',
            obj.body
        )

    def email_data(self, obj):
        return pretty_json(obj.data)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
