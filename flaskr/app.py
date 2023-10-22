
from flask_restful import Resource, Api
from flask_cors import CORS
from flask import Flask, request, json
from flask_middleware_jwt import Middleware
from flask_jwt_extended import JWTManager
from .utils.json_custom_encoder import JSONCustomEncoder
from .dataContext.sqlAlchemyContext import db
import requests
from flaskr import create_app
from config import Config
from .views import HealthCheckView, LogInView, SignUpView, TokenVerifyView,ConversionView

config = Config()


app = create_app('default')
app.json_encoder = JSONCustomEncoder

app_context = app.app_context()
app_context.push()

db.init_app(app)
db.create_all()

cors = CORS(app)

api = Api(app)

#resources
api.add_resource(HealthCheckView, '/health')
api.add_resource(LogInView, '/api/auth/login')
api.add_resource(SignUpView, '/api/auth/signup')
api.add_resource(TokenVerifyView, '/api/token/verify')
api.add_resource(ConversionView, '/api/tasks')

jwt = JWTManager(app)