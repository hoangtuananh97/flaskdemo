from flask import request
from flask_accepts import responds
from flask_restx import Resource

from app.api.blueprint.account import AccountBlueprint
from app.api.service.account.user import login, register
from app.core.decorators import accepts
from app.schema.requests.users.user import (
    LoginRequestSchema,
    RegisterAccountRequestSchema,
)
from app.schema.response.users.user import UserLoginResponseSchema, UserResponseSchema

api = AccountBlueprint.api


@api.route("/login/")
class AccountLogin(Resource):
    @accepts(
        api=api,
        schema=LoginRequestSchema,
    )
    @responds(schema=UserLoginResponseSchema)
    def post(self):
        post_data = request.get_json()
        username = post_data.get("username")
        password = post_data.get("password")
        return login(username, password)


@api.route("/register/")
class Register(Resource):
    @accepts(
        api=api,
        schema=RegisterAccountRequestSchema,
    )
    @responds(schema=UserResponseSchema)
    def post(self):
        post_data = request.get_json()
        username = post_data.get("username")
        password = post_data.get("password")
        return register(username, password)
