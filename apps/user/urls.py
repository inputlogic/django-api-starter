from django.urls import path

from apps.user.endpoints.public.login.views import PublicLoginView
from apps.user.endpoints.public.signup.views import PublicSignupView
from apps.user.endpoints.public.forgot_password_step_1.views import PublicForgotPasswordStep1View
from apps.user.endpoints.public.forgot_password_step_2.views import PublicForgotPasswordStep2View
from apps.user.endpoints.user.change_password.views import UserChangePasswordView
from apps.user.endpoints.user.change_email.views import UserChangeEmailView
from apps.user.endpoints.user.my_profile.views import UserMyProfileView

urlpatterns = [
    path('public/user/login', PublicLoginView.as_view(),
         name='public-user-login'),
    path('public/user/signup', PublicSignupView.as_view(),
         name='public-user-signup'),
    path('public/user/forgot-password-step-1', PublicForgotPasswordStep1View.as_view(),
         name='public-user-forgot-password-step-1'),
    path('public/user/forgot-password-step-2', PublicForgotPasswordStep2View.as_view(),
         name='public-user-forgot-password-step-2'),
    path('user/change-password', UserChangePasswordView.as_view(),
         name='user-change-password'),
    path('user/change-email', UserChangeEmailView.as_view(),
         name='user-change-email'),
    path('user/my-profile', UserMyProfileView.as_view(),
         name='user-my-profile'),
]
