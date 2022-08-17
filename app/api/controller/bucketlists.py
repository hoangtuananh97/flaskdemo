from flask import request
from flask_accepts import responds
from flask_restx import Resource

from app.api.blueprint.bucketlist import BucketListsBlueprint
from app.api.service.bucketlists.bucketlist import (
    create_bucketlist,
    delete_bucketlist,
    get_bucketlist_detail,
    get_list_from_filter,
    update_bucketlist,
)
from app.core.common.utils import login_required
from app.core.decorators import accepts
from app.core.validators.validate import ValidateObjectExistByID
from app.schema.requests.bucketlists.buckketlist import (
    BucketListFilterSchema,
    CreateBucketListRequestSchema,
)
from app.schema.response.bucketlists.bucketlist import (
    BucketListResponseSchema,
    FilterBucketListList,
)

api = BucketListsBlueprint.api


@api.route("")
class BucketLists(Resource):
    @login_required
    @accepts(
        api=api,
        schema=CreateBucketListRequestSchema,
    )
    @responds(schema=BucketListResponseSchema)
    def post(self):
        return create_bucketlist(**request.get_json())

    @login_required
    @accepts(api=api, schema=BucketListFilterSchema, has_request_params=True)
    @responds(schema=FilterBucketListList)
    def get(self):
        input_params = request.args.to_dict()
        response_data = get_list_from_filter(input_params)
        return response_data


@api.route("/<int:bucketlist_id>")
class BucketListsDetail(Resource):
    @responds(schema=BucketListResponseSchema)
    def put(self, bucketlist_id):
        validator = ValidateObjectExistByID()
        bucketlist = validator(BucketLists, id=bucketlist_id, name="id")
        return update_bucketlist(bucketlist, request.get_json())

    @responds(schema=BucketListResponseSchema)
    @login_required
    def get(self, bucketlist_id):
        return get_bucketlist_detail(bucketlist_id, request.current_user.id)

    @login_required
    def delete(self, bucketlist_id):
        validator = ValidateObjectExistByID()
        bucketlist = validator(BucketLists, id=bucketlist_id, name="id")
        return delete_bucketlist(bucketlist)
