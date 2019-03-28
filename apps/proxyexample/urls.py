from django.urls import path

from . import views

urlpatterns = [
    path('proxy/users', views.ProxyUserList.as_view(), name='proxy-user-list'),
]
