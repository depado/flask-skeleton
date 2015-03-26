# -*- coding: utf-8 -*-

import logging
from logging.handlers import RotatingFileHandler

from flask import Flask
from werkzeug.contrib.fixers import ProxyFix

# App Initialization
app = Flask(__name__)
app.config.from_object('config')
app.wsgi_app = ProxyFix(app.wsgi_app)

# Jinja2 Setup
app.jinja_env.trim_blocks = True

# Logging with Rotating File Setup
handler = RotatingFileHandler(app.config.get('LOG_FILE'), maxBytes=10000, backupCount=5)
handler.setLevel(logging.DEBUG)
handler.setFormatter(
    logging.Formatter(fmt='%(asctime)s %(name)s[%(process)d] %(levelname)s %(message)s', datefmt='%b %d %H:%M:%S')
)
app.logger.addHandler(handler)

from app import views
