from os import environ
import os

class Config:
    # General
    FLASK_DEBUG = False)

    # Database
    APP_BASEDIR = os.path.dirname(__file__)
    SQLALCHEMY_DATABASE_URI='sqlite:///../db/app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    NEWSAPI_KEY='e3591106e13347bc92a3d1ab29a5c341'