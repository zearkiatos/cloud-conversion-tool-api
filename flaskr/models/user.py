from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from ..dataContext.sqlAlchemyContext import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64))
    password = db.Column(db.String(32))

class UserSchema(SQLAlchemyAutoSchema):

    class Meta:
        model = User
        include_relationships = True
        load_instance = True