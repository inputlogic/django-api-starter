from django.urls import path

from . import views

urlpatterns = [
    path('me', views.Me.as_view(), name='me'),
    path('users', views.UserList.as_view(), name='user-list'),
    path('auth/signup', views.UserCreate.as_view(), name='signup'),
    path('auth/login', views.UserCustomObtainAuthToken.as_view(), name='login'),
    path('auth/forgot-password', views.UserForgotPassword.as_view(), name='forgot-password'),
    path('auth/reset-password', views.UserResetPassword.as_view(), name='reset-password')
]
