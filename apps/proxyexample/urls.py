from django.urls import path

from . import views, views_with_logging

urlpatterns = [
    path('proxy/users', views.ProxyUserList.as_view(), name='proxy-user-list'),
    path(
        'proxy/logging/users',
        views_with_logging.ProxyUserList.as_view(),
        name='proxy-user-list-logging'
    )
]
