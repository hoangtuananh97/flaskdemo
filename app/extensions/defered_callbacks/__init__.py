from app.extensions.defered_callbacks.after_request import (
    add_cors,
    close_database,
    record_request_duration,
)
from app.extensions.defered_callbacks.before_request import record_request


def register_deferred_callbacks(app):
    app.before_request_funcs = {
        None: [
            record_request,
        ]
    }

    app.after_request_funcs = {
        None: [
            add_cors,
            close_database,
            record_request_duration,  # need to be the last one
        ]
    }
