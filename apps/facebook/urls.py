from django.urls import path

from . import views

urlpatterns = [
    path('facebook/url', views.LoginURL.as_view(), name='facebook-login-url'),
    path('facebook/code', views.CodeExchange.as_view(), name='facebook-code-exchange'),
]
