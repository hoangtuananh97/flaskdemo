from marshmallow import validates_schema
from marshmallow.fields import String, Integer

from app.api.model import Users
from app.core.validators.validate import ValidateObjectExistByID
from app.schema.requests.base import BaseRequestSchema


class CreateBucketListRequestSchema(BaseRequestSchema):

    name = String(required=True)
    completed_by = Integer(required=True)
    owner_id = Integer(required=True)

    @validates_schema()
    def validate_data(self, data, **kwargs):
        validator = ValidateObjectExistByID()
        validator(Users, id=data.get("owner_id"), name="owner_id")
        validator(Users, id=data.get("completed_by"), name="completed_by")


class BucketListFilterSchema(BaseRequestSchema):
    name = String()
    page = Integer(required=True)
    size = Integer(required=True)
    total = Integer()
