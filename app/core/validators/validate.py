from enum import Enum
from typing import Type

from marshmallow import ValidationError
from marshmallow.validate import Email, Length, Regexp, Validator

from .validate_error_code import ValidateErrorCode


class ValidateLength(Length):
    message_min = ValidateErrorCode.MIN_LENGTH
    message_max = ValidateErrorCode.MAX_LENGTH

    def __call__(self, value):
        length = len(value)

        if self.equal is not None:
            self.min = self.equal
            self.max = self.equal

        if self.min is not None and length < self.min:
            message = self.message_min
            raise ValidationError(self._format_error(value, message))

        if self.max is not None and length > self.max:
            message = self.message_max
            raise ValidationError(self._format_error(value, message))

        return value


class ValidateRange(Length):
    default_message = ValidateErrorCode.INVALID_FORMAT

    def __call__(self, value):
        if self.min > value:
            raise ValidationError(self.default_message)
        return value


class ValidateNumbersAndLettersOnly(Regexp):
    default_message = ValidateErrorCode.INVALID_FORMAT
    regex = "^[A-Za-z0-9]*$"

    def __init__(self):
        super().__init__(self.regex)


class ValidateNumbersOnly(Regexp):
    default_message = ValidateErrorCode.INVALID_FORMAT
    regex = "^[0-9]*$"

    def __init__(self):
        super().__init__(self.regex)


class ValidateEnum(Validator):
    default_message = ValidateErrorCode.INVALID_TYPE

    def __init__(self, enum: Type[Enum]):
        self.enum = enum.__dict__

    def __call__(self, value):
        if value not in self.enum:
            raise ValidationError(self.default_message)


class ValidateEmail(Email):
    default_message = ValidateErrorCode.INVALID_FORMAT


class ValidateList(Validator):
    def __call__(self, values):
        if not len(values):
            raise ValidationError(ValidateErrorCode.IS_REQUIRED)


class CustomDBValidator(Validator):
    def __call__(self, *args, **kwargs):
        model_name = args[0]
        self.validator_model = kwargs.pop("validator_model", ValidationError)
        self.model_name = model_name
        self.query = model_name.query
        return kwargs


class CustomValidateWithDelete(CustomDBValidator):
    def __call__(self, *args, **kwargs):
        kwargs = super().__call__(*args, **kwargs)
        self.query = self.model_name.query

        if getattr(self.model_name, "deleted_by", None):
            self.query = self.query.filter_by(deleted_date=None, deleted_by=None)
        return kwargs


class ValidateObjectExistByID(CustomValidateWithDelete):
    def __call__(self, model_name, **kwargs):
        kwargs = super().__call__(model_name, **kwargs)

        self.query = self.query.filter_by(id=kwargs.get("id"))
        data = self.query.first()
        if not data:
            raise self.validator_model(
                "{} {}".format(kwargs.get("name", ""), ValidateErrorCode.NOT_EXIST)
            )
        return data


class ValidateObjectExistByIDWithDelete(CustomValidateWithDelete):
    def __call__(self, model_name, **kwargs):
        kwargs = super().__call__(model_name, **kwargs)

        data = self.query.filter_by(id=kwargs.get("id")).first()
        if not data:
            raise self.validator_model(
                "{} {}".format(kwargs.get("name", ""), ValidateErrorCode.NOT_EXIST)
            )
        return data


class ValidateFieldUniqueExist(CustomDBValidator):
    def __call__(self, model_name, **kwargs):
        kwargs = super().__call__(model_name, **kwargs)
        filter_dict = {kwargs.get("field_name"): kwargs.get("value")}
        self.query = self.query.filter_by(**filter_dict)
        data = self.query.first()
        if data:
            raise self.validator_model(
                "{} {}".format(kwargs.get("value", ""), ValidateErrorCode.EXISTED)
            )
        return data
