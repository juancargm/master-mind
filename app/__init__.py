""" Initialize Application. """
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


def init_app(test_config=None) -> Flask:
    """ Initialize the core application. """
    app = Flask(__name__, instance_relative_config=False)

    if test_config is None:
        # Read from the config object
        app.config.from_object('config.Config')
    else:
        # Load the test config if passed in
        app.config.update(test_config)

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
