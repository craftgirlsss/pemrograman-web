# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask_login import UserMixin
from sqlalchemy.orm import relationship
from flask_dance.consumer.storage.sqla import OAuthConsumerMixin

from apps import db, login_manager

from apps.authentication.util import hash_pass

class Users(db.Model, UserMixin):
    __tablename__ = 'Users'

    id            = db.Column(db.Integer, primary_key=True)
    username      = db.Column(db.String(64), unique=True)
    first_name    = db.Column(db.String(100), nullable=True)
    last_name     = db.Column(db.String(100), nullable=True)
    address       = db.Column(db.String(100), nullable=True)
    bio           = db.Column(db.String(200), nullable=True)
    email         = db.Column(db.String(64), unique=True)
    password      = db.Column(db.LargeBinary)

    oauth_github  = db.Column(db.String(100), nullable=True)

    api_token     = db.Column(db.String(100))
    api_token_ts  = db.Column(db.Integer)    

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            if hasattr(value, '__iter__') and not isinstance(value, str):
                value = value[0]

            if property == 'password':
                value = hash_pass(value)

            setattr(self, property, value)

    def __repr__(self):
        return str(self.username)
    
    @staticmethod
    def find_by_username(username):
        return Users.query.filter_by(username=username).first()
    
    @staticmethod
    def find_by_email(email):
        return Users.query.filter_by(email=email).first()


@login_manager.user_loader
def user_loader(id):
    return Users.query.filter_by(id=id).first()


@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    user = Users.query.filter_by(username=username).first()
    return user if user else None

class OAuth(OAuthConsumerMixin, db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey("Users.id", ondelete="cascade"), nullable=False)
    user = db.relationship(Users)
    