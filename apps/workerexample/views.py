from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from . import tasks


class SayHello(GenericAPIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        tasks.say_hello(name=request.query_params.get('name', 'Dude'))
        return Response({'ok': True})


class Fail(GenericAPIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        tasks.failing_task()
        return Response({'ok': True})
