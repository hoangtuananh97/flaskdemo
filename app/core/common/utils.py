""" utility functions """
from functools import wraps

from flask import request

from app.api.model.account.user import Users
from app.core.exceptions.un_authorized import UnauthorizedException


def login_required(function):
    """utility  decorator function to check is users is authenticated"""

    @wraps(function)
    def decorated(*args, **kwargs):
        """decorator function logic"""
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            raise UnauthorizedException(message="Provide valid auth Token")
        auth_token = auth_header.split(" ")[1]
        user_id = Users.decode_auth_token(auth_token)
        if isinstance(user_id, str):
            raise UnauthorizedException(message=user_id)
        user = Users.query.filter_by(id=user_id).first()
        if not user:
            raise UnauthorizedException(message=user_id)
        return function(user, *args, **kwargs)

    return decorated
