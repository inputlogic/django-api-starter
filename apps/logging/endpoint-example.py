from django.contrib.auth import get_user_model
from django.urls import path
from rest_framework import generics, permissions
from rest_framework_tracking.mixins import LoggingMixin

from apps.user.serializers import UserSerializer


class LoggedUserList(LoggingMixin, generics.ListAPIView):
    '''
    An example of a logged API endpoint
    '''

    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAdminUser,)

    # LoggingMixin options:
    logging_methods = ['GET','POST']
    sensitive_fields = {'password'}

    def should_log(self, request, response):
        # For example, only log on errors
        return response.status_code >= 400

    def handle_log(self):
        if self.log['response_ms'] > 1000:
            # Do something
            pass

        return super().handle_log()


urlpatterns = [
    path('api/logged-users-example', LoggedUserList.as_view(), name='logged-user-list-example'),
]
