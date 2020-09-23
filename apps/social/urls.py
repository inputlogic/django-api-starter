from django.urls import path

from . import views

urlpatterns = [
    path('auth/facebook', views.auth_facebook, name='auth-facebook'),
    path('auth/google', views.auth_google, name='auth-google'),
]
