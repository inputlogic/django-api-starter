from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^files$', views.CreateSignedFile.as_view(), name='file-signed-url'),
    url(r'^files/(?P<pk>[0-9]+)/?$', views.FileDetail.as_view(), name='file-detail')
]
