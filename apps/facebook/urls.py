from django.urls import path

from . import views

urlpatterns = [
    path('facebook/url', views.LoginURL.as_view(), name='facebook-login-url'),
    path(
        'facebook/code/fb-token',
        views.CodeForFacebookToken.as_view(),
        name='facebook-code-for-facebook-token'
    ),
    path(
        'facebook/code/token',
        views.CodeForAccessToken.as_view(),
        name='facebook-code-for-access-token'
    ),
    path(
        'facebook/fb-token/token',
        views.FacebookTokenForAccessToken.as_view(),
        name='facebook-token-for-access-token'
    ),
]
