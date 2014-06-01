import os

basedir = os.path.abspath(os.path.dirname(__file__))
CSRF_ENABLED = True
SECRET_KEY = 'itsnotreallyasecretyouknow'
DEBUG = True

os.urandom(32).encode('hex')