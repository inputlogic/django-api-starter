from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from libs.access import access_to_drf

from .views import api_root


admin.site.site_title = settings.ADMIN_TITLE
admin.site.site_header = settings.ADMIN_HEADER

access_urls = access_to_drf(None, None)
# access_urls = []

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # Apps
    path('', include('apps.file.urls')),
    path('', include('apps.user.urls')),

    # DRF API
    path('api/', api_root, name='index'),
    path('api-auth/', include('rest_framework.urls')),
    *access_urls
]

print('yo', urlpatterns)
