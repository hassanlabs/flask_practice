from flask import Flask
from .extensions import db
from .routes.routes import authentication
from flasgger import Swagger  # Import Swagger
import jwt


def create_app(config_name=None):
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    db.init_app(app)
    # Initialize Swagger
    swagger = Swagger(app)
    app.register_blueprint(authentication)

    with app.app_context():
        db.create_all()
    return app
