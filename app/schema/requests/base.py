# coding=utf-8

from marshmallow import Schema
from marshmallow.fields import Boolean, Date, Field, Integer, List, String

from app.core.validators.validate_error_code import ValidateErrorCode


class BaseRequestSchema(Schema):
    Field.default_error_messages["required"] = ValidateErrorCode.IS_REQUIRED
    String.default_error_messages["invalid"] = ValidateErrorCode.INVALID_TYPE
    Integer.default_error_messages["invalid"] = ValidateErrorCode.INVALID_TYPE
    Boolean.default_error_messages["invalid"] = ValidateErrorCode.INVALID_TYPE
    Date.default_error_messages["invalid"] = ValidateErrorCode.INVALID_FORMAT
    List.default_error_messages["invalid"] = ValidateErrorCode.INVALID_TYPE
    Schema._default_error_messages["unknown"] = ValidateErrorCode.UNKNOWN_FIELD
