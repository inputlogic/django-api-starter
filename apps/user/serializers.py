from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.tokens import default_token_generator
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ParseError

from . import emails


class UserSerializer(serializers.ModelSerializer):
    is_admin = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = get_user_model()
        fields = ('id', 'email', 'password', 'is_admin')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def get_is_admin(self, obj):
        return obj.is_staff

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = get_user_model()(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, obj, validated_data):
        password = validated_data.pop('password', None)
        if password:
            obj.set_password(password)
        return super().update(obj, validated_data)


class CustomAuthTokenSerializer(serializers.Serializer):
    '''
    Modified from rest_framework.authtoken.serializers.AuthTokenSerializer
    to accept email field instead of username
    '''
    email = serializers.CharField(label=_("Email"))
    password = serializers.CharField(
        label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'),
                                username=email, password=password)

            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "email" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)

    def create(self, validated_data):
        email = validated_data['email']
        try:
            user = get_user_model().objects.get(email=email)
        except get_user_model().DoesNotExist:
            return {}

        reset_token = default_token_generator.make_token(user)
        emails.forgot_password(reset_token, user)
        return {}


class ResetPasswordSerializer(serializers.Serializer):
    token = serializers.CharField(write_only=True)
    user_id = serializers.IntegerField(write_only=True)
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        token = validated_data['token']
        user_id = validated_data['user_id']
        password = validated_data['password']

        user = get_user_model().objects.get(id=user_id)
        if not default_token_generator.check_token(user, token):
            raise ParseError(detail='Invalid token')

        user.set_password(password)
        user.save()
        return {}
