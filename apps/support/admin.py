from django.contrib import admin

from rest_framework_tracking.models import APIRequestLog
from rest_framework_tracking.admin import APIRequestLogAdmin

admin.site.unregister(APIRequestLog)

'''
Out of the box DRF Tracking doesn't make IP address a searchable field.
For trouble shooting a specific user this is very useful. Therefore, use
a proxy class and add remote_attr as a search field.
'''

class DSAPIRequestLog(APIRequestLog):
    class Meta:
        proxy = True

@admin.register(DSAPIRequestLog)
class DSAPIRequestLogAdmin(admin.ModelAdmin):
    date_hierarchy = 'requested_at'
    list_display = ('id', 'requested_at', 'response_ms', 'status_code',
                    'user', 'method',
                    'path', 'remote_addr', 'host',
                    'query_params')
    list_filter = ('method', 'status_code')
    search_fields = ('path', 'user__email', 'remote_addr')
    raw_id_fields = ('user', )

    #Proxy models have a bug where their permissions don't work. Allow all.
    def has_change_permission(self, request, obj=None):
        return True
