from typing import Type, Union

from flask_accepts.decorators.decorators import for_swagger, get_default_model_name
from flask_restx import reqparse
from marshmallow import Schema, ValidationError

from app.core.exceptions.schema_validation import SchemaValidationException


def _is_method(func):
    """
    Check is function is defined inside a class.
    ASSUMES YOU ARE USING THE CONVENTION THAT FIRST ARG IS 'self'
    """
    import inspect

    sig = inspect.signature(func)
    return "self" in sig.parameters


def accepts(
    schema: Union[Schema, Type[Schema], None] = None,
    model_name: str = None,
    many: bool = False,
    has_request_params: bool = False,
    has_request_form_data: bool = False,
    api=None,
):
    schema = _get_or_create_schema(schema, many=many)

    if api:
        _parser = api.parser()
    else:
        _parser = reqparse.RequestParser(bundle_errors=True)

    def decorator(func):
        from functools import wraps

        # Check if we are decorating a class method
        _IS_METHOD = _is_method(func)

        @wraps(func)
        def inner(*args, **kwargs):
            from flask import request

            if has_request_params:
                try:
                    obj = schema.load(request.args)
                    request.parse_args = obj
                except ValidationError as err:
                    raise SchemaValidationException(
                        message="Not Found", extra=err.messages
                    )
            elif has_request_form_data:
                try:
                    obj = schema.load(request.form)
                    request.parse_obj = obj

                except ValidationError as err:
                    raise SchemaValidationException(
                        message="Not Found", extra=err.messages
                    )
            else:
                try:
                    obj = schema.load(request.get_json())
                    request.parse_obj = obj
                except ValidationError as err:
                    raise SchemaValidationException(
                        message="Not Found", extra=err.messages
                    )

            return func(*args, **kwargs)

        # Add Swagger
        if api and _IS_METHOD:
            if schema:
                body = for_swagger(
                    schema=schema,
                    model_name=model_name or get_default_model_name(schema),
                    api=api,
                    operation="load",
                )
                if schema.many is True:
                    body = [body]

                params = {
                    "expect": [body, _parser],
                }
                inner = api.doc(**params)(inner)
            elif _parser:
                inner = api.expect(_parser)(inner)

        return inner

    return decorator


def _get_or_create_schema(
    schema: Union[Schema, Type[Schema]], many: bool = False
) -> Schema:
    if isinstance(schema, Schema):
        return schema
    return schema(many=many)
