from os import environ
import os

class Config:
    """Set Flask configuration vars from .env file."""

    # General
    FLASK_DEBUG = environ.get('FLASK_DEBUG')

    # Database
    APP_BASEDIR = os.path.dirname(__file__)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(APP_BASEDIR, 'db', 'app.db') #environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = environ.get('SQLALCHEMY_TRACK_MODIFICATIONS')
    NEWSAPI_KEY = environ.get('NEWAPI_KEY')