from flask_accepts import responds
from flask_restx import Resource

from app.api.blueprint.account import AccountBlueprint
from app.api.service.account.user import login
from app.core.decorators import accepts
from app.schema.requests.users.user import LoginRequestSchema
from app.schema.response.users.user import UserResponseSchema
from flask import request

api = AccountBlueprint.api


@api.route("/login/")
class Account(Resource):
    @accepts(api=api, schema=LoginRequestSchema,)
    @responds(schema=UserResponseSchema)
    def post(self):
        post_data = request.get_json()
        username = post_data.get("username")
        password = post_data.get("password")
        return login(username, password)
