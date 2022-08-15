from flask_restx import Namespace


class AccountBlueprint:
    api = Namespace("account", description="api account")
