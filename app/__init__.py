""" __init__.py """

from flasgger import Swagger
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate

from app.extensions import setup_extensions
from app.extensions.bcrypt import bcrypt
from app.extensions.database import db
from config import config

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
    from app.api.blueprint import blueprint

    app.register_blueprint(blueprint)
    setup_extensions(app)

    return app
