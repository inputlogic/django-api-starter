from django.core.exceptions import ValidationError as DjangoValidationError

from rest_framework import status
from rest_framework.exceptions import ValidationError as DRFValidationError
from rest_framework.response import Response
from rest_framework.views import exception_handler as drf_exception_handler


def exception_handler(exc, context):
    """
    Handle Django ValidationError as an accepted exception
    Must be set in settings:
    >>> REST_FRAMEWORK = {
    ...     # ...
    ...     'EXCEPTION_HANDLER': 'libs.exception_handler.exception_handler',
    ...     # ...
    ... }
    For the parameters, see ``exception_handler``
    """

    if isinstance(exc, DjangoValidationError):
        if hasattr(exc, 'message_dict'):
            exc = DRFValidationError(detail=exc.message_dict)
        else:
            exc = DRFValidationError(detail=exc.message)

    return drf_exception_handler(exc, context)


def unknown_exception_handler(exception):
    return Response(
        {"error": str(exception)},
        status=status.HTTP_500_INTERNAL_SERVER_ERROR
    )
