from django.contrib.auth import get_user_model
from rest_framework import generics, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.authtoken.models import Token


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


class UserList(generics.ListAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)


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
