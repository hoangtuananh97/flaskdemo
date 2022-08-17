import time
import uuid

from flask import g


def record_request():
    """
    Establish the request an UUID and record start time

    :return: None
    """
    g.request_id = uuid.uuid4()
    g.request_start_time = time.time()
