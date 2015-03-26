# -*- coding: utf-8 -*-

from app import app

@app.route('/', methods=['GET'])
def index():
    return "<h1>Hello World</h1>"
