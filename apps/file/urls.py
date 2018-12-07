from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^files$', views.CreateSignedFile.as_view(), name='file-signed-url'),
]
