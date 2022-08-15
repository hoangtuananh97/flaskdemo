from http import HTTPStatus

from app.core.error_messages import ErrorMessages
from app.core.exceptions import APIException


class SchemaValidationException(APIException):
    message = ErrorMessages.not_found
    http_status = HTTPStatus.NOT_FOUND

    def __init__(self, message=ErrorMessages.bad_request, extra=None):
        super().__init__(http_status=HTTPStatus.NOT_FOUND, message=message, extra=extra)

    def __str__(self):
        return "schema validation errors"


class ValidatorException(APIException):
    message = ErrorMessages.not_found
    http_status = HTTPStatus.NOT_FOUND

    def __init__(self, message=ErrorMessages.not_found):
        super().__init__(http_status=HTTPStatus.NOT_FOUND, message=message)

    def __str__(self):
        return "not found error"
