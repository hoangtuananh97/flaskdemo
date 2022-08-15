""" __init__.py """

from flasgger import Swagger
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from config import config

db = SQLAlchemy()
bcrypt = Bcrypt()
migrate = Migrate()
swagger = Swagger()


def create_app(config_name):
    """Application Factory"""
    # instantiate the app
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    # set up the extensions
    CORS(app)
    db.init_app(app)
    bcrypt.init_app(app)
    swagger.init_app(app)
    migrate.init_app(app, db)

    # register blueprints
    from app.api.auth import auth_blueprint
    from app.api.bucketlists import bucketlist_blueprint

    app.register_blueprint(auth_blueprint, url_prefix="/auth")
    app.register_blueprint(bucketlist_blueprint, url_prefix="/bucketlists")

    return app
