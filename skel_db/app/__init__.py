# -*- coding: utf-8 -*-

from flask.ext.sqlalchemy import SQLAlchemy
from flask import Flask
from werkzeug.contrib.fixers import ProxyFix

app = Flask(__name__)
app.config.from_object('config')
app.wsgi_app = ProxyFix(app.wsgi_app)
db = SQLAlchemy(app)

from app import views, models
