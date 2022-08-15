from flask import Blueprint
from flask_restx import Api

from app.api.controller.account import api as account_ns

blueprint = Blueprint("api", __name__)

api = Api(
    blueprint,
    title="",
    version="1.0",
    description="",
)

api.add_namespace(account_ns, path="/api/accounts/")
