import facebook
from django.conf import settings
from rest_framework import generics, permissions, status
from rest_framework.response import Response
import urllib.parse as urlparse

from .serializers import (
    FacebookCodeExchangeSerializer
)


def _get_facebook_login_url():
    graph = facebook.GraphAPI(
        access_token=settings.FACEBOOK_APP_CLIENT_TOKEN,
        version=settings.FACEBOOK_GRAPH_VERSION
    )

    perms = ["email"]
    fb_login_url = graph.get_auth_url(
        settings.FACEBOOK_APP_ID, settings.FACEBOOK_SUCCESSFUL_LOGIN_URL,
        perms
    )
    return fb_login_url


class LoginURL(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, *args, **kwargs):
        facebook_login_url = _get_facebook_login_url()
        return Response({"result": facebook_login_url}, status.HTTP_200_OK)


class CodeExchange(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = FacebookCodeExchangeSerializer

    '''
        public function getUserIdFromCode($code)
        {
            $loginUrl = $this->getLoginUrl('?preview=1');
            $parts = parse_url($loginUrl);
            parse_str($parts['query'], $query);
            $redirectUrl = $query['redirect_uri'];
            $path = 'https://graph.facebook.com/v'.facebook::GRAPH_VERSION.'/oauth/access_token';
            $path .= '?client_id='.facebook::getAppId();
            $path .= '&redirect_uri='.$redirectUrl;
            $path .= '&client_secret='.facebook::getAppSecret();
            $path .= '&code='.$code;
            $result = $this->fetchFBData($path);
            $token = $result['access_token'];
            $user_id = $this->getUserIdFromToken($token);
            return $user_id;
        }

    '''

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response({'error': serializer.errors}, status.HTTP_400_BAD_REQUEST)
        code = serializer.validated_data['code']
        facebook_login_url = _get_facebook_login_url()
        parsed = urlparse.urlparse(facebook_login_url)
        redirect_uri = urlparse.parse_qs(parsed.query)['redirect_uri'][0]
        path = (
            'https://graph.facebook.com/v%s/oauth/access_token'
            '?client_id=%s'
            '&redirect_uri=%s'
            '&client_secret=%s'
            '&code=%s'
        ) % (
            settings.FACEBOOK_GRAPH_VERSION,
            settings.FACEBOOK_APP_ID,
            redirect_uri,
            settings.FACEBOOK_APP_SECRET,
            code
        )

        return Response({"result": path}, status.HTTP_200_OK)
        '''
        print ('facebook_login_url')
        facebook_login_url
        oauth_args = dict(
            client_id = FACEBOOK_APP_ID,
            client_secret = FACEBOOK_APP_SECRET,
            grant_type = 'client_credentials')
        graph = facebook.GraphAPI(
            access_token=settings.FACEBOOK_APP_CLIENT_TOKEN,
            version=settings.FACEBOOK_GRAPH_VERSION
        )
        # app_id = "1231241241"
        # canvas_url = "https://domain.com/that-handles-auth-response/"
        perms = ["email"]
        fb_login_url = graph.get_auth_url(
            settings.FACEBOOK_APP_ID, settings.FACEBOOK_SUCCESSFUL_LOGIN_URL,
            perms
        )
        return Response({"result": fb_login_url}, status.HTTP_200_OK)
        '''
