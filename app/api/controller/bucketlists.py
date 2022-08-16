from flask import request
from flask_accepts import responds
from flask_restx import Resource

from app.api.blueprint.bucketlist import BucketListsBlueprint
from app.api.service.bucketlists.bucketlist import get_bucketlist_detail
from app.core.common.utils import login_required
from app.schema.response.bucketlists.bucketlist import BucketListResponseSchema

api = BucketListsBlueprint.api


@api.route("")
class BucketLists(Resource):
    @login_required
    def post(self):
        pass

    @login_required
    def get(self):
        pass


@api.route("/<int:bucket_list_id>")
class BucketListsDetail(Resource):
    def put(self):
        pass

    @responds(schema=BucketListResponseSchema)
    @login_required
    def get(self, bucketlist_id):
        data = request.data
        return get_bucketlist_detail(bucketlist_id, "user_id")

    @login_required
    def delete(self):
        pass
