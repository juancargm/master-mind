""" Initialize Application. """
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


def init_app() -> Flask:
    """ Initialize the core application. """
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')

    db.init_app(app)

    with app.app_context():
        """ Prepare the application. """
        # Create tables for our models
        from app import models
        db.create_all()

        # Include the Controllers
        from app import controllers
        app.register_blueprint(controllers.endpoint_bp)
        
        return app
