# -*- coding: utf-8 -*-

from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash

from app import app, db


class User(db.Model):
    """
    User model. Integrates with Flask-Login.

    id: The ID of the user.
    username: The username of the user (can contain any characters)
    password: Encrypted password
    superuser: Boolean to tell if the user is a superuser
    active: Boolean to tell if the user is active (ability to login and operate on the app)
    register_date: The date the user registered
    last_login: The date the user last logged in the app
    """

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(54))
    superuser = db.Column(db.Boolean())
    active = db.Column(db.Boolean())
    register_date = db.Column(db.DateTime())
    last_login = db.Column(db.DateTime())

    def __init__(self, username, password, superuser=False, active=True, register_date=None, last_login=None):
        """
        :param username: The username of the user.
        :param password: The raw password to be encrypted and stored.
        :param active: Set if the user is active or not (restrains from logging for example)
        :param superuser: Set if the user is a superuser
        :param register_date: Set the date of registration (defaults to "now")
        :param last_login:
        """
        now = datetime.utcnow()
        self.username = username
        self.set_password(password)
        self.superuser = superuser
        self.active = active
        if register_date:
            self.register_date = register_date
        else:
            self.register_date = now
        if last_login:
            self.last_login = last_login
        else:
            self.last_login = now

    def save(self):
        """
        Save method. Allows to easily save a single object.
        Also logs the errors in case of Exception.
        Customise this method to suit your needs.
        :return: True if the operation succeed, False otherwise.
        """
        db.session.add(self)
        try:
            db.session.commit()
        except Exception as e:
            app.logger.exception("Something went wrong while saving a user {}".format(e))
            db.session.rollback()
            return False
        return True

    def delete(self):
        """
        Delete method allows to easily delete a single object.
        Also logs the errors in case of Exception.
        Customise this method to suit your needs.
        :return: True if the operation succeed, False otherwise.
        """
        db.session.delete(self)
        try:
            db.session.commit()
        except Exception as e:
            app.logger.exception("Something went wrong while deleting a user {}".format(e))
            db.session.rollback()
            return False
        return True

    def is_superuser(self):
        return self.superuser

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def is_authenticated(self):
        return True

    def is_active(self):
        return self.active

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def __repr__(self):
        return "User(id={!r self.id}, username={!r self.username}, superuser={!r self.superuser}, " \
               "active={!r self.active}, register_date={!r self.register_date}, last_login={!r self.last_login}".format(
                   self=self
               )

    def __str__(self):
        return self.username
