""" BucketList Models """
import datetime
import jwt
from flask import current_app
from . import db, bcrypt


class Users(db.Model):
    """ Model for users """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True,
                         index=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    bucket_lists = db.relationship(
        'BucketLists', backref="owner", lazy="dynamic", cascade="delete, delete-orphan")

    def __init__(self, username, password):
        self.username = username
        self.password = bcrypt.generate_password_hash(
            password, current_app.config.get('BCRYPT_LOG_ROUNDS')
        ).decode()

    def encode_auth_token(self, user_id):
        """ Generates auth token """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(
                    days=current_app.config.get('TOKEN_EXPIRATION_DAYS'),
                    seconds=current_app.config.get('TOKEN_EXPIRATION_SECONDS')),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                current_app.config.get('SECRET_KEY'),
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """ Decodes the authentication token """
        try:
            payload = jwt.decode(
                auth_token,
                current_app.config.get('SECRET_KEY'))
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Expired token. Please Log in again'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again'


class BucketLists(db.Model):
    """ Model for bucket lists """
    __tablename__ = 'bucketlists'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False, unique=True)
    completed_by = db.Column(db.Integer, nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    bucket_lists_items = db.relationship(
        'BucketListItems', backref="bucket_list", lazy="dynamic", cascade="delete, delete-orphan")

    def to_json(self):
        """ Convert bucket list model to json format """
        json_data = {
            'id': self.id,
            'name':self.name,
            'completed_by': self.completed_by,
            'items': [item.to_json() for item in self.bucket_lists_items.all()]
        }
        return json_data


class BucketListItems(db.Model):
    """ Model for bucket list items """
    __tablename__ = "bucketlistitems"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    completed = db.Column(db.Boolean, default=False, nullable=False)
    bucketlist_id = db.Column(db.Integer, db.ForeignKey('bucketlists.id'))

    def to_json(self):
        """ Convert bucket list item model to json format """
        json_data = {
            'id' : self.id,
            'name' :self.name,
            'completed' : self.completed
        }
        return json_data
