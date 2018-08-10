from django.urls import path

from . import views


urlpatterns = [
    path('say-hello', views.SayHello.as_view(), name='say-hello'),
    path('fail', views.Fail.as_view(), name='fail'),
]
