
from .views import HealthCheckView
from flask_restful import Resource, Api
from flask import Flask, request, json
from flask_middleware_jwt import Middleware
import requests
from flaskr import create_app
from config import Config

config = Config()


app = create_app('default')

app_context = app.app_context()
app_context.push()
api = Api(app)

#resources
api.add_resource(HealthCheckView, '/health')