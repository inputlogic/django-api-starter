from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^me$', views.Me.as_view(), name='me'),
    url(r'^users$', views.List.as_view(), name='user-list'),
    url(r'^auth/signup$', views.Create.as_view(), name='signup'),
    url(r'^auth/login$', views.CustomObtainAuthToken.as_view(), name='login'),
]
