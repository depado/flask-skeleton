# -*- coding: utf-8 -*-

from flask import render_template

from app import app

@app.route('/', methods=['GET'])
def index():
    return "<h1>Hello World</h1>"