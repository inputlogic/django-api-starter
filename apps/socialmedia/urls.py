from django.urls import path

from . import views

urlpatterns = [
    path('facebook/url', views.LoginURL.as_view(), name='facebook-login-url'),
    path(
        'facebook/authcode/fb-token',
        views.AuthCodeForFacebookToken.as_view(),
        name='facebook-authcode-for-facebook-token'
    ),
    path(
        'facebook/authcode/token',
        views.AuthCodeForAccessToken.as_view(),
        name='facebook-authcode-for-access-token'
    ),
    path(
        'facebook/fb-token/token',
        views.FacebookTokenForAccessToken.as_view(),
        name='facebook-token-for-access-token'
    ),
    path('google/url', views.LoginURL.as_view(), name='google-login-url'),
    path(
        'google/authcode/google-token',
        views.AuthCodeForGoogleToken.as_view(),
        name='google-authcode-for-google-token'
    ),
    path(
        'google/authcode/token',
        views.AuthCodeForAccessToken.as_view(),
        name='google-authcode-for-access-token'
    ),
    path(
        'google/google-token/token',
        views.GoogleTokenForAccessToken.as_view(),
        name='google-token-for-access-token'
    )
]
