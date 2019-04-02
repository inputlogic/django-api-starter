import facebook
from django.conf import settings
from rest_framework import generics, permissions, status
from rest_framework.response import Response


class LoginURL(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, *args, **kwargs):
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
