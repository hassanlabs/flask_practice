from flask import Flask
from .extensions import db
from .routes.routes import authentication  # Make sure this points to your Blueprint

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')  # Ensure this is correct

    db.init_app(app)

    app.register_blueprint(authentication)  # Register the Blueprint

    with app.app_context():
        db.create_all()  # Create database tables

    return app
