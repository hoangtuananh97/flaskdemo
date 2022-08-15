from http import HTTPStatus

from app.core.error_messages import ErrorMessages
from app.core.exceptions import APIException


class UnauthorizedException(APIException):
    message = ErrorMessages.un_authorized
    http_status = HTTPStatus.UNAUTHORIZED

    def __init__(self, message=ErrorMessages.un_authorized, extra=None):
        super().__init__(http_status=HTTPStatus.UNAUTHORIZED, message=message, extra=extra)

    def __str__(self):
        return "Unauthorized"
