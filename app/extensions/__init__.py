def setup_extensions(app):
    from app.extensions.defered_callbacks import register_deferred_callbacks

    from .error_handlers import register_error_handler

    register_error_handler(app)
    register_deferred_callbacks(app)
