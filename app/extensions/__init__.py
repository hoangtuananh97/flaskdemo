def setup_extensions(app):
    from .error_handlers import register_error_handler

    register_error_handler(app)
