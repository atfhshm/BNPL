from typing import Any

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler


def server_error_handler(exc: Exception, context: dict[str, Any]) -> Response:
    response = exception_handler(exc, context)
    if response is None:
        return Response(
            {'detail': 'Internal server error: ' + str(exc)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    return response
