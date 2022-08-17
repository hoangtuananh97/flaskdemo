from app import bcrypt
from app.api.model.account.user import Users
from app.core.common.common import add_user
from app.core.exceptions.bad_request import BadRequestException
from app.core.exceptions.un_authorized import UnauthorizedException


def login(username, password):
    try:
        user = Users.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            auth_token = user.encode_auth_token(user.id)
            if auth_token:
                return {"token": auth_token}
        raise UnauthorizedException()
    except Exception:
        raise UnauthorizedException()


def register(username, password):
    try:
        user = add_user(username, password)
        return {"id": user.id, "username": user.username}
    except Exception:
        raise BadRequestException()
