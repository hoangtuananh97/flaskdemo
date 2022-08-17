from marshmallow.fields import Integer, String

from app.schema.response.base import BaseResponseSchema


class UserResponseSchema(BaseResponseSchema):
    class Meta:
        ordered = True

    id = Integer(required=True)
    username = String(required=True)


class UserLoginResponseSchema(BaseResponseSchema):
    id = Integer(required=True)
    username = String(required=True)
    token = String(required=True)
