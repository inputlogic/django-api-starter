import json
import requests

from libs.exception_handler import unknown_exception_handler
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework_tracking.mixins import LoggingMixin

from .serializers import (
    ProxyUserListSerializer
)


class ProxyLoggingMixin(LoggingMixin):
    def finalize_proxy_response(self, request, prepared_request, response, *args, **kwargs):
        self.log.update(
            {
                'remote_addr': self._get_ip_address(request),
                'view': self._get_view_name(request),
                'view_method': self._get_view_method(prepared_request),
                'path': prepared_request.url,
                'host': request.get_host(),
                'method': prepared_request.method,
                'query_params': self._clean_data(request.query_params.dict()),
                'user': self._get_user(request),
                'response_ms': self._get_response_ms(),
                'response': self._clean_data(response.content.decode("utf-8")),
                'status_code': response.status_code,
                'data': prepared_request.body.decode("utf-8")
            }
        )
        self.handle_log()
        return response


'''
Example of proxy API call. This is an endpoint being called from within an endpoint. Common when
integrating third party APIs.
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
            params = ('id', '100')
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
            prepared_request = requests.Request('get', path, params={'id':'123'}, headers=headers, json=body).prepare()
            response = requests.get(path, headers=headers, data=body)
            self.finalize_proxy_response(request, prepared_request, response, *args, **kwargs)
            result = json.loads(response.content.decode("utf-8"))
        except Exception as e:
            return unknown_exception_handler(e)

        return Response({"result": result}, status.HTTP_200_OK)
