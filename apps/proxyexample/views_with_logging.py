import json

from libs.exception_handler import unknown_exception_handler
from libs.proxy_logging import ProxyLoggingMixin
from rest_framework import generics, permissions, status
from rest_framework.response import Response

from .serializers import (
    ProxyUserListSerializer
)


'''
Example of proxy API call with logging. This is an endpoint being called from within an endpoint.
This is useful when you need to monitor the data moving back and forth from your server to a third
party API. In could me necessary as an audit trail.
'''


class ProxyUserList(ProxyLoggingMixin, generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ProxyUserListSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response({'error': serializer.errors}, status.HTTP_400_BAD_REQUEST)

        try:
            '''
            This code is verbose on purpose for reference. API key and auth token are included
            for reference as well.

            api keys, URLs and auth tokens would not normally be stored here, but rather in an
            environment variable specific to a staging or production server instancese.

            The auth_token could be a permanent token, or there could be additional logic for
            re generating expired tokens.
            '''
            path = 'https://jsonplaceholder.typicode.com/users'
            '''
            #error test
            path = 'http://www.mocky.io/v2/5c9e9556300000af21ee98ab'
            '''
            params = {'sort': 'asc', 'limit': 100}
            api_key = '123456789'
            auth_token = 'abcdefghi'
            headers = {
                'Content-Type': 'application/json',
                'X-Auth-API-Key': api_key,
                'authorization': 'Bearer ' + auth_token
            }
            body = {
                "company_id": 12,
                "department": "accounting"
            }
            response = self.with_log(request, 'get', path, headers, body, params)
            result = json.loads(response.content.decode("utf-8"))
        except Exception as e:
            return unknown_exception_handler(e)

        return Response({"result": result}, status.HTTP_200_OK)
