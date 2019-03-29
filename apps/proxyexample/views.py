import json
import requests

from libs.exception_handler import unknown_exception_handler
from rest_framework import generics, permissions, status
from rest_framework.response import Response

from .serializers import (
    ProxyUserListSerialzier
)

'''
Example of proxy API call. This is an endpoint being called from within an endpoint. Common when
integrating third party APIs.
'''


class ProxyUserList(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ProxyUserListSerialzier

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

            response = requests.get(path, headers=headers, data=body)
            result = json.loads(response.content.decode("utf-8"))
        except Exception as e:
            return unknown_exception_handler(e)

        return Response({"result": result}, status.HTTP_200_OK)
