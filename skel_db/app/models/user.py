# -*- coding: utf-8 -*-

from datetime import datetime
from werkzeug import generate_password_hash, check_password_hash
from app import db

class Permission(object):
    allowed = "A"
    denied = "D"
    restricted = "R"


class User(db.Model):
    """
    A simple user model with permission handling and password hash.
    Implements two methods to set the password and check the password.
    """
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(54))
    permission = db.Column(db.String(1))

    def __init__(self, email, username, password):
        self.username = username.lower()
        self.email = email.lower()
        self.set_password(password)
        self.permission = Permission.allowed

    def set_password(self, password):
        self.passwordhash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.passwordhash, password)