from http import HTTPStatus

from app.core.error_messages import ErrorMessages


class APIException(Exception):
    """ "
    Base class for all handled exception on API
    ...
    Attributes
    ----------
    http_status: HTTPStatus
        one of HTTPStatus which will be
    message: str
        brief message described the error
        can use `APICode.description` as default message
    extra: dict
        extra information related to the error
    """

    http_status = HTTPStatus.INTERNAL_SERVER_ERROR
    message = ErrorMessages.default
    data = None
    extra = None
    success = False

    def __init__(
        self,
        success=False,
        data=None,
        http_status=HTTPStatus.INTERNAL_SERVER_ERROR,
        message=ErrorMessages.default,
        extra=None,
    ):
        """
        Parameters
        ----------
        :param code: APICode
            one of APICode which summarize result of operation
        :param http_status: HTTPStatus
            one of HTTPStatus which will be
        :param message: str
            brief message described the error
            can use `APICode.description` as default message
        :param extra: dict
            extra information related to the error
        """
        super().__init__()
        self.success = success
        self.data = data
        self.http_status = http_status
        self.message = message
        self.extra = extra
