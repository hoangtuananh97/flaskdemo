from marshmallow import validates_schema
from marshmallow.fields import String

from app.core.validators.validate import ValidateFieldUniqueExist
from app.api.model.account.user import Users
from app.schema.requests.base import BaseRequestSchema


class LoginRequestSchema(BaseRequestSchema):

    username = String(required=True)
    password = String(required=True)
