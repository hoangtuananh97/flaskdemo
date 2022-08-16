from marshmallow import Schema
from marshmallow.fields import Integer, Nested, String

from app.schema.response.base import BaseResponseSchema


class UserSchemaType(Schema):
    class Meta:
        ordered = True

    id = Integer(required=True)
    username = String(required=True)


class BucketListResponseSchema(BaseResponseSchema):
    class Meta:
        ordered = True

    id = Integer(required=True)
    name = String(required=True)
    completed_by = Nested(UserSchemaType)
    owner = Nested(UserSchemaType)
