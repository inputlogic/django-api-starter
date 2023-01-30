from rest_framework import views, permissions
from rest_framework.response import Response
from rest_framework.parsers import FormParser, MultiPartParser

from .serializers import HTMLArraySerializer


class HTMLArray(views.APIView):
    """
    An example of handling an array of fields posted from an HTML form:

    <input type="text" name="foods[]" value="pizza" />
    <input type="text" name="foods[]" value="sushi" />

    """
    permission_classes = [permissions.AllowAny]
    parser_classes = [FormParser, MultiPartParser]

    def post(self, request, format=None):
        data = request.data.copy()
        data['foods'] = request.data.getlist('foods[]')  # Must be converted to list, not QueryDict
        serializer = HTMLArraySerializer(data)

        # Here we're just returning the value for visibility, but you would normally use the
        # serializer to insert into db.
        return Response(serializer.data)
