import logging
import traceback
from http import HTTPStatus

from flask import g
from werkzeug.exceptions import HTTPException

from app.extensions.error import Error
from app.core.exceptions import APIException

logger = logging.getLogger("app")


def register_error_handler(app):
    # TODO: Log exception and notify engineers
    app.register_error_handler(Exception, application_error_handler)


def application_error_handler(exception):
    if isinstance(exception, APIException):
        return api_error_handler(exception)

    if isinstance(exception, HTTPException):
        return werkzeug_http_error_handler(exception)

    return unknown_error_handler(exception)


def api_error_handler(exception):
    response = {
        "success": exception.success,
        "message": exception.message,
        "data": exception.data,
    }

    if exception.extra is not None:
        response["extra"] = exception.extra

    return response, exception.http_status


def werkzeug_http_error_handler(exception):
    logger.error(traceback.format_exc())
    response = {"data": None, "success": False, "message": exception.description}

    return response, exception.code


def unknown_error_handler(exception):
    error = Error(g.request_id, str(exception), traceback.format_exc())

    logging.critical(str(error))
    response = {"data": None, "message": str(exception), "success": False}

    return response, HTTPStatus.INTERNAL_SERVER_ERROR
