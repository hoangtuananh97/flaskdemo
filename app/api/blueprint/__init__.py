from flask import Blueprint
from flask_restx import Api

from app.api.controller.account import api as account_ns
from app.api.controller.bucketlists import api as bucket_list_ns

blueprint = Blueprint("api", __name__)

api = Api(
    blueprint,
    title="",
    version="1.0",
    description="",
)

api.add_namespace(account_ns, path="/api/accounts")
api.add_namespace(bucket_list_ns, path="/api/bucketlists")
