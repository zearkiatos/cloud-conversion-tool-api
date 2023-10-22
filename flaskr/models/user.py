from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from sqlalchemy.orm import validates
import re
from ..dataContext.sqlAlchemyContext import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64))
    password1 = db.Column(db.String(15))
    password2 = db.Column(db.String(15))
    email = db.Column(db.String(64))

    def __init__(self, username, password1, password2, email):
        self.username = username
        self.password1 = password1
        self.password2 = password2
        self.email = email

        if self.password1 != self.password2:
            raise ValueError(
                'The password and confirmation password are not the same')

    @validates('username')
    def username_validation(self, key, username):
        if type(username) is not str or username == '':
            raise ValueError('The username should be a valid string')
        if len(username) > 65:
            raise ValueError('The username should be maximam 64 characters')

        return username

    @validates('password1')
    def password1_validation(self, key, password1):
        if type(password1) is not str or password1 == '':
            raise ValueError('The password should be a valid string')

        if not re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[$@$!%*?&_.])([A-Za-z\d$@$!%*?&_.]|[^ ]){8,15}$", password1):
            raise ValueError(
                'The password should be valid password minimal one lowercase letter, one uppercase letter,  one number and one special character between [$@$!%*?&_.] and minimal 8 character and maximan 15')

        return password1

    @validates('email')
    def email_validation(self, key, email):
        if type(email) is not str and email == '':
            raise ValueError('The email should be a valid string')

        if not re.match(r"[a-z0-9]+@[a-z]+\.[a-z]{2,3}", email):
            raise ValueError(
                'The email should be a valid email example@mail.com')

        return email


class UserSchema(SQLAlchemyAutoSchema):

    class Meta:
        model = User
        include_relationships = True
        load_instance = True
