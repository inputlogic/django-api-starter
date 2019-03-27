from django.contrib.auth import get_user_model
from rest_framework import generics, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework_tracking.mixins import LoggingMixin

from .serializers import (
    UserSerializer,
    ForgotPasswordSerializer,
    ResetPasswordSerializer
)


class Me(generics.RetrieveUpdateDestroyAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()
        return


class UserCreate(generics.CreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)


class UserList(LoggingMixin, generics.ListAPIView):
    # optionally specify what methods to log
    # logging_methods = ['GET','POST']
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)

    '''
    optional mask sensitive data. By default drf-tracking is hiding the
    values of the fields {'api', 'token', 'key', 'secret', 'password', 'signature'}.
    '''
    sensitive_fields = {'password'}

    # Optional set conditions for when logging should occur
    '''
    def should_log(self, request, response):
        return response.status_code >= 400
    '''

    # Optional custom handler logic
    '''
    def handle_log(self):
        #Save only very slow requests. Requests that took more than a second.
        if self.log['response_ms'] > 1000:
    '''


class UserCustomObtainAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        return Response({'token': token.key, 'userId': token.user_id})


class UserForgotPassword(generics.CreateAPIView):
    serializer_class = ForgotPasswordSerializer
    permission_classes = (permissions.AllowAny,)


class UserResetPassword(generics.CreateAPIView):
    serializer_class = ResetPasswordSerializer
    permission_classes = (permissions.AllowAny,)
