from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow 

db = SQLAlchemy()
ma = Marshmallow()

def create_app():
    """Construct the core application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')
    db.init_app(app)
    ma.init_app(app)
    
    with app.app_context():
        # Imports
        from . import routes

        # Create tables for our models
        db.create_all()

        return app