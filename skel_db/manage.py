# -*- coding: utf-8 -*-

from flask_script import Manager

from app import app, db

manager = Manager(app)

@manager.command
def create_db():
    db.create_all()

if __name__ == "__main__":
    manager.run()
