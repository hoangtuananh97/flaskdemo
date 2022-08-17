import logging
import time

from flask import current_app, g, request
from flask_sqlalchemy import get_debug_queries
from sqlalchemy.orm import Query

from app.extensions.database import db

logger = logging.getLogger(__name__)


def record_request_duration(response):
    """
    Record execution time of the reuqest

    :param response:
    :return: response:
    """
    g.request_end_time = time.time()
    g.request_duration = (g.request_end_time - g.request_start_time) * 1000

    return response


def add_cors(response):
    response.headers["Access-Control-Allow-Origin"] = "*"

    response.headers["Access-Control-Allow-Credentials"] = "true"
    response.headers[
        "Access-Control-Allow-Methods"
    ] = "GET,POST,OPTIONS,PUT,DELETE,PATCH"
    response.headers["Access-Control-Allow-Headers"] = (
        "Authorization,Accept,Origin,DNT,X-CustomHeader,Keep-Alive,User-Agent,"
        "X-Requested-With,If-Modified-Since,Cache-Control,"
        "Content-Type,Content-Range,Range, X-CSRF-Token"
    )

    return response


def log_queries(response):
    """
    Log queries which are executed during the request

    :param response:
    :return: response:
    """
    if current_app.config["FEATURES"].get("log_queries"):
        for query in get_debug_queries():
            logger.info(str(Query(g.request_id, query)))

    return response


def close_database(response):
    db.session.close()
    return response
