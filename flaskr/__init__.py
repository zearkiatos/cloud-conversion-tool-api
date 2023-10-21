from flask import Flask
from config import Config


def create_app(config_name):
    config = Config()
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI']=config.DATA_BASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
    return app

from .app import *