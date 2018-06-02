from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import RedirectView
from django.urls import reverse_lazy

from .views import api_root


urlpatterns = [
    # API Index
    url(r'^$', api_root, name='index'),

    # Admin
    url(r'^admin/$', RedirectView.as_view(url=reverse_lazy('admin:user_user_changelist'))),
    url(r'^admin/', admin.site.urls),
    url(r'^jet/', include('jet.urls', 'jet')),

    # App routes
    url(r'^', include('apps.user.urls')),
    url(r'^', include('apps.content.urls')),

    # DRF Browseable-API Auth
    url(r'^api-auth/', include('rest_framework.urls')),
]

if settings.ENV == settings.DEV:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
