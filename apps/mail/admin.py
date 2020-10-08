from django.contrib import admin
from django.utils.html import format_html, mark_safe

from .models import Mail, Template, Layout
from .libs.pretty_json import make_pretty_json


@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'subject', 'created_at')
    fields = ('name', 'last_data_sent', 'example_data', 'layout', 'body', 'subject', 'preview')
    readonly_fields = ('name', 'last_data_sent', 'example_data', 'created_at', 'preview')

    def last_data_sent(self, obj):
        return make_pretty_json(obj.last_email_sent.data) if obj.last_email_sent else ''

    def example_data(self, obj):
        return make_pretty_json(obj.data_example) if obj.data_example else ''

    def preview(self, obj):
        data = obj.last_email_sent.data if obj.last_email_sent else obj.data_example
        layout = obj.layout.html if obj.layout else '{body}'
        return mark_safe(
            '''
                <div>
                    <br />
                    <h3>Subject</h3>
                    <br />
                    {0}
                    <br /><br />
                    <h3>Body</h3>
                    <br />
                    {1}
                </div>
            '''.format(
                obj.render(obj.subject, data),
                layout.format(body=obj.render(obj.body, data))
            )
        )


@admin.register(Layout)
class LayoutAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')


@admin.register(Mail)
class MailAdmin(admin.ModelAdmin):
    list_display = ('subject', 'email', 'name', 'status', 'created_at')
    fieldsets = (
        (None, {
            'fields': ('name', 'user', 'email_subject', 'email_body', 'status'),
        }),
        ('Technical', {
            'fields': ('email_data', 'api_response_code', 'api_response_text'),
            'classes': ('collapse',),
        }),
    )
    readonly_fields = ('email_subject', 'email_body', 'email_data')

    def email_subject(self, obj):
        return format_html('{0}', obj.subject)

    def email_body(self, obj):
        return format_html(
            '<iframe srcdoc="{0}" style="width: 100%; height: 800px; border: 1px solid #f0f0f0" ></iframe>',
            obj.body
        )

    def email_data(self, obj):
        return make_pretty_json(obj.data)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
