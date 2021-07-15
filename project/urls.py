from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from .views import api_root


admin.site.site_title = settings.ADMIN_TITLE
admin.site.site_header = settings.ADMIN_HEADER


urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # Apps
    path('', include('apps.file.urls')),
    path('', include('apps.socialmedia.urls')),
    path('', include('apps.user.urls')),

    # Example Apps
    #  path('', include('apps.proxyexample.urls')),
    #  path('', include('apps.workerexample.urls')),
    #  path('', include('apps.logging.endpoint-example')),

    # DRF API
    path('api/', api_root, name='index'),
    path('api-auth/', include('rest_framework.urls')),
]

#  if settings.ENV == settings.DEV:
#      urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
#      urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
