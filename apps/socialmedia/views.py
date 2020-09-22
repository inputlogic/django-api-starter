import facebook
import json
import requests

from django.conf import settings
from libs.exception_handler import unknown_exception_handler
from libs.proxy_logging import ProxyLoggingMixin
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

import google_auth_oauthlib.flow

from apps.socialmedia.models import SocialMedia
from apps.user.models import User

from .serializers import (
    CodeExchangeSerializer,
    FacebookTokenExchangeSerializer,
    GoogleTokenExchangeSerializer
)


def _get_social_media_for_user(user):
    try:
        social_media = SocialMedia.objects.get(user=user)
        return social_media
    except SocialMedia.DoesNotExist:
        return None


def _get_social_media_for_identifier(source, identifier):
    try:
        if(identifier):
            social_media = SocialMedia.objects.get(source=source, identifier=identifier)
            return social_media
    except SocialMedia.DoesNotExist:
        return None


# Get the Facebook login URL
class FacebookLoginURL(ProxyLoggingMixin, generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, *args, **kwargs):
        try:
            graph = facebook.GraphAPI(
                access_token=settings.FACEBOOK_APP_CLIENT_TOKEN,
                version=settings.FACEBOOK_GRAPH_VERSION
            )

            perms = ["email"]
            fb_login_url = graph.get_auth_url(
                settings.FACEBOOK_APP_ID, settings.FACEBOOK_SUCCESSFUL_LOGIN_URL,
                perms
            )
        except Exception as e:
            return unknown_exception_handler(e)

        return Response({"result": fb_login_url}, status.HTTP_200_OK)


# Have a Facebook auth code, want a facebook user token
class AuthCodeForFacebookToken(ProxyLoggingMixin, generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = CodeExchangeSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response({'error': serializer.errors}, status.HTTP_400_BAD_REQUEST)
        try:
            # submit the auth code to facebook for a facebook user token
            code = serializer.validated_data['code']
            path = (
                'https://graph.facebook.com/v%s/oauth/access_token' %
                (settings.FACEBOOK_GRAPH_VERSION)
            )

            params = {
                'client_id': settings.FACEBOOK_APP_ID,
                'redirect_uri': settings.FACEBOOK_SUCCESSFUL_LOGIN_URL,
                'client_secret': settings.FACEBOOK_APP_SECRET,
                'code': code
            }

            response = self.with_log(request, 'post', path, {}, {}, params)
            result = json.loads(response.content.decode("utf-8"))

            if response.status_code != status.HTTP_200_OK:
                return Response({"result": result}, response.status_code)

            access_token = result['access_token']
            return Response({"result": {"facebook_user_token": access_token}}, status.HTTP_200_OK)
        except Exception as e:
            return unknown_exception_handler(e)


# Exchange the Facebook user token for a Django access token. Create the user if they don't exist.
def _facebookTokenForAccessToken(facebook_user_token):
    try:
        graph = facebook.GraphAPI(
            access_token=facebook_user_token,
            version=settings.FACEBOOK_GRAPH_VERSION
        )

        args = {'fields': 'id, name, email', }
        try:
            fb_user_result = graph.get_object('me', **args)
        except facebook.GraphAPIError as e:
            return Response({"error": e.__dict__['result']['error']}, status.HTTP_400_BAD_REQUEST)

        email = fb_user_result['email']
        identifier = fb_user_result['id']
        social_media = _get_social_media_for_identifier(
            source=SocialMedia.FACEBOOK,
            identifier=identifier
        )

        if(social_media is not None):
            user = social_media.user
        else:
            # get or create the user
            user, created = User.objects.get_or_create(email=email)
            if created:
                social_media = SocialMedia.objects.create(
                    user=user,
                    source=SocialMedia.FACEBOOK,
                    identifier=identifier
                )
            else:
                '''
                The user was found, but does not have a matching social media token. Return an
                error indicating the user should login with the origin source.
                '''
                social_media = _get_social_media_for_user(user=user)
                if social_media is None:
                    result = {
                        "error": "Please login with username and password"
                    }
                else:
                    result = {
                        "error": "Please login with " + SocialMedia.SOCIAL_MEDIA_SOURCES[social_media.source][1]
                    }
                return Response(result, status.HTTP_400_BAD_REQUEST)

        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key, "user_id": user.id}, status.HTTP_200_OK)
    except Exception as e:
        raise e


# Have a Facebook auth code, want a Django access token
class FacebookAuthCodeForAccessToken(ProxyLoggingMixin, generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = CodeExchangeSerializer

    def post(self, request, *args, **kwargs):
        try:
            # re-use the end point for obtaining the facebook user token
            view = AuthCodeForFacebookToken.as_view()(self.request._request)

            # if something went wrong, pass along the bad news
            if view.status_code != status.HTTP_200_OK:
                return view
            result = view.data['result']
            facebook_user_token = result['facebook_user_token']
            # have a facebook user token, exchange it for a Django access token
            return _facebookTokenForAccessToken(facebook_user_token)
        except Exception as e:
            return unknown_exception_handler(e)


# Have a Facebook user token, want a Django access token. Create the user if they don't exist.
class FacebookTokenForAccessToken(ProxyLoggingMixin, generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = FacebookTokenExchangeSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response({'error': serializer.errors}, status.HTTP_400_BAD_REQUEST)

        try:
            # have a facebook user token, exchange it for a Django access token
            facebook_user_token = serializer.validated_data['facebook_user_token']
            return _facebookTokenForAccessToken(facebook_user_token)
        except Exception as e:
            return unknown_exception_handler(e)


def _googleFlow():
    CLIENT_CONFIG = {
        'web': {
            'client_id': settings.GOOGLE_CLIENT_ID,
            'project_id': settings.GOOGLE_PROJECT_ID,
            'auth_uri': 'https://accounts.google.com/o/oauth2/auth',
            'token_uri': 'https://oauth2.googleapis.com/token',
            'auth_provider_x509_cert_url': 'https://www.googleapis.com/oauth2/v1/certs',
            'client_secret': settings.GOOGLE_CLIENT_SECRET,
            'redirect_uris': [settings.GOOGLE_REDIRECT_URI]
        }
    }
    # Use the information in the CLIENT_CONFIG to identify
    # the application requesting authorization.
    flow = google_auth_oauthlib.flow.Flow.from_client_config(
        client_config=CLIENT_CONFIG,
        scopes=[
            'https://www.googleapis.com/auth/userinfo.profile',
            'https://www.googleapis.com/auth/userinfo.email'
        ]
    )

    # Indicate where the API server will redirect the user after the user completes
    # the authorization flow. The redirect URI is required.
    flow.redirect_uri = settings.GOOGLE_SUCCESSFUL_LOGIN_URL
    return flow


# Get the Google login URL
class GoogleLoginURL(ProxyLoggingMixin, generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, *args, **kwargs):
        flow = _googleFlow()

        # Generate URL for request to Google's OAuth 2.0 server.
        # Use kwargs to set optional request parameters.
        authorization_url, state = flow.authorization_url(
            # Enable offline access so that you can refresh an access token without
            # re-prompting the user for permission. Recommended for web server apps.
            access_type='offline',
            # Enable incremental authorization. Recommended as a best practice.
            include_granted_scopes='true'
        )

        return Response({"result": authorization_url}, status.HTTP_200_OK)


# Have a Google auth code, want a google user token
class AuthCodeForGoogleToken(ProxyLoggingMixin, generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = CodeExchangeSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response({'error': serializer.errors}, status.HTTP_400_BAD_REQUEST)
        try:
            flow = _googleFlow()
            # submit the auth code to Google for a Google user token
            code = serializer.validated_data['code']
            try:
                flow.fetch_token(code=code)
            except Exception as e:
                return unknown_exception_handler(e)
            google_user_token = flow.credentials.__dict__['token']

            # access_token = result['access_token']
            return Response(
                {"result": {"google_user_token": google_user_token}},
                status.HTTP_200_OK
            )
        except Exception as e:
            return unknown_exception_handler(e)


# Exchange the Google user token for a Django access token. Create the user if they don't exist.
def _googleTokenForAccessToken(google_user_token):
    try:
        headers = {"Authorization": "OAuth %s" % google_user_token}
        response = requests.get(
            "https://www.googleapis.com/oauth2/v2/userinfo",
            headers=headers
        )

        google_user_result = json.loads(response.content.decode("utf-8"))

        if response.status_code != status.HTTP_200_OK:
            return Response(google_user_result, response.status_code)

        email = google_user_result['email']
        identifier = google_user_result['id']
        social_media = _get_social_media_for_identifier(
            source=SocialMedia.GOOGLE,
            identifier=identifier
        )

        if(social_media is not None):
            user = social_media.user
        else:
            # get or create the user
            user, created = User.objects.get_or_create(email=email)
            if created:
                social_media = SocialMedia.objects.create(
                    user=user,
                    source=SocialMedia.GOOGLE,
                    identifier=identifier
                )
            else:
                # The user was found, but does not have a matching social media token. Return an
                # error indicating the user should login with the origin source.
                social_media = _get_social_media_for_user(user=user)
                if social_media is None:
                    result = {
                        "error": "Please login with username and password"
                    }
                else:
                    result = {
                        "error": "Please login with " + SocialMedia.SOCIAL_MEDIA_SOURCES[social_media.source][1]
                    }
                return Response(result, status.HTTP_400_BAD_REQUEST)

        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key, "user_id": user.id}, status.HTTP_200_OK)
    except Exception as e:
        raise e


# Have a Google auth code, want a Django access token
class GoogleAuthCodeForAccessToken(ProxyLoggingMixin, generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = CodeExchangeSerializer

    def post(self, request, *args, **kwargs):
        try:
            # re-use the end point for obtaining the facebook user token
            cfgt = AuthCodeForGoogleToken.as_view()(self.request._request)

            # if something went wrong, pass along the bad news
            if cfgt.status_code != status.HTTP_200_OK:
                return cfgt
            result = cfgt.data['result']
            google_user_token = result['google_user_token']
            # have a Google user token, exchange it for a Django access token
            return _googleTokenForAccessToken(google_user_token)
        except Exception as e:
            return unknown_exception_handler(e)


# Have a Google user token, want a Django access token. Create the user if they don't exist.
class GoogleTokenForAccessToken(ProxyLoggingMixin, generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = GoogleTokenExchangeSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response({'error': serializer.errors}, status.HTTP_400_BAD_REQUEST)

        try:
            # have a Google user token, exchange it for a Django access token
            google_user_token = serializer.validated_data['google_user_token']
            print('google_user_token')
            print(google_user_token)
            return _googleTokenForAccessToken(google_user_token)
        except Exception as e:
            return unknown_exception_handler(e)
