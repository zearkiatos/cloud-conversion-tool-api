from flask_restful import Resource
import json
from flask import request, jsonify
from http import HTTPStatus
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from datetime import datetime
from ...dataContext import db
from ...models.user import User, UserSchema
from config import Config

config = Config()

class LogInView(Resource):
    def post(self):
        try:
            username = request.json['username']
            password = request.json['password']
            user = User.query.filter_by(username=username, password1=password).all()
            if user:
                args = (username, datetime.utcnow())
                access_token = create_access_token(identity=user[0].id)
                return {"message": "Login session successful", "accessToken": access_token}, HTTPStatus.OK
            else:
                return {"message": "User name or password wrong"}, HTTPStatus.UNAUTHORIZED
        except Exception as ex:
            print(f"Error: {str(ex)}")
            return {
                "message": "Something was wrong 🤯",
                "error": str(ex)
            }, HTTPStatus.INTERNAL_SERVER_ERROR
        
class SignUpView(Resource):
    def post(self):
        try:
            user = User.query.filter((User.username == request.json["username"]) | (User.email == request.json["email"])).first()
            if not user:
                new_user = User(
                    username=request.json["username"], password1=request.json["password1"], password2=request.json["password2"], email=request.json["email"])
                access_token = create_access_token(identity=request.json['username'])
                db.session.add(new_user)
                db.session.commit()
                return {
                    "message": "Created user successful",
                    "accessToken": access_token
                }, HTTPStatus.OK
            else:
                return {
                    "message": "The user exist"
                }, HTTPStatus.CONFLICT
        except ValueError as ex:
            return {
                "message": str(ex),
            }, HTTPStatus.BAD_REQUEST
        except Exception as ex:
            print(f"Error: {str(ex)}")

            return {
                "message": "Something was wrong 🤯",
                "error": str(ex)
            }, HTTPStatus.INTERNAL_SERVER_ERROR
        
class TokenVerifyView(Resource):
    @jwt_required()
    def get(self):
        try:
            return {"message": "Authorization Valid"}, HTTPStatus.OK
        except Exception as ex:
            print(f"Error: {str(ex)}")
            return {
                "message": "Something was wrong 🤯",
                "error": str(ex)
            }, HTTPStatus.INTERNAL_SERVER_ERROR