from http import HTTPStatus

from app.core.error_messages import ErrorMessages
from app.core.exceptions import APIException


class NotFoundException(APIException):
    message = ErrorMessages.not_found
    http_status = HTTPStatus.NOT_FOUND

    def __init__(self, message=ErrorMessages.not_found, extra=None):
        super().__init__(http_status=HTTPStatus.NOT_FOUND, message=message, extra=extra)

    def __str__(self):
        return "Not Found errors"
