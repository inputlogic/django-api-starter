from django.contrib import admin
from rest_framework_tracking.admin import APIRequestLogAdmin as BaseAPIRequestLogAdmin
from rest_framework_tracking.models import APIRequestLog as BaseAPIRequestLog

from .models import APIRequestLog


admin.site.unregister(BaseAPIRequestLog)
@admin.register(APIRequestLog)
class APIRequestLogAdmin(BaseAPIRequestLogAdmin):
    '''
    Override default admin to make remote_addr (ie IP address) searchable
    '''
    search_fields = ('path', 'user__email', 'remote_addr')

    def has_add_permission(self, request):
        '''
        If you are manually populating your API logs... something isn't right.
        '''
        return False

    def has_change_permission(self, request, obj=None):
        '''
        Avoid temptation to tamper with the logs
        '''
        return False
