from app import bcrypt
from app.api.model.account.user import Users
from app.core.exceptions.un_authorized import UnauthorizedException


def login(username, password):
    try:
        user = Users.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            auth_token = user.encode_auth_token(user.id)
            if auth_token:
                return {
                    "token": auth_token.decode()
                }
        raise UnauthorizedException()
    except Exception:
        raise UnauthorizedException()
