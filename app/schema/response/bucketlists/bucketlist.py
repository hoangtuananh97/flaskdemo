from marshmallow import Schema
from marshmallow.fields import Integer, List, Nested, String

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


class FilterBucketListSchema(Schema):
    class Meta:
        ordered = True

    id = Integer(required=True)
    person_id = String(required=True)
    prefix = String()
    firstname = String(required=True)


class FilterBucketListList(BaseResponseSchema):
    class Meta:
        ordered = True

    items = List(Nested(FilterBucketListSchema))
    total = Integer(required=True)
    page_size = Integer(required=True)
    page = Integer(required=True)
