from marshmallow import validates_schema
from marshmallow.fields import String

from app.api.model.account.user import Users
from app.core.validators.validate import ValidateFieldUniqueExist
from app.schema.requests.base import BaseRequestSchema


class LoginRequestSchema(BaseRequestSchema):

    username = String(required=True)
    password = String(required=True)


class RegisterAccountRequestSchema(BaseRequestSchema):

    username = String(required=True)
    password = String(required=True)

    @validates_schema()
    def validate_data(self, data, **kwargs):
        validator = ValidateFieldUniqueExist()
        validator(Users, field_name="username", value=data.get("password"))
