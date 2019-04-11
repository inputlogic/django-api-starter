from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin


admin.site.site_title = settings.ADMIN_TITLE
admin.site.site_header = settings.ADMIN_HEADER


urlpatterns = [
    # Admin
    url(r'^admin/', admin.site.urls),

    # App routes
    url(r'^', include('apps.content.urls')),
    url(r'^', include('apps.facebook.urls')),
    url(r'^', include('apps.file.urls')),
    url(r'^', include('apps.socialmedia.urls')),
    url(r'^', include('apps.user.urls')),

    # ___CHANGEME___
    # Routes for example apps
    url(r'^', include('apps.proxyexample.urls')),
    url(r'^', include('apps.workerexample.urls')),
]

if settings.ENV == settings.DEV:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
