#!/usr/bin/env python3
# coding=utf-8

from flask import Flask, jsonify
from werkzeug.local import LocalStack, LocalProxy

from ext import db
from users import User

_user_stack = LocalStack()

app = Flask(__name__, template_folder=".")
app.config.from_object("config")
db.init_app(app)

def get_current_user():
    top = _user_stack.top
    if top is None:
        raise RuntimeError()
    return top

current_user = LocalProxy(get_current_user)

@app.before_first_request
def setup():
    db.drop_all()
    db.create_all()
    fake_users = [
        User("xiaoming", "xiaoming@github.com"),
        User("xiaohua", "xiaohua@github.com"),
        User("xiaozhang", "xiaozhang@github.com"),
    ]
    db.session.add_all(fake_users)
    db.session.commit()

@app.before_request
def before_request():
    user = User.query.filter_by(id=1).one()
    _user_stack.push(user)

@app.teardown_appcontext
def teardown(exc=None):
    if exc is None:
        db.session.commit()
    else:
        db.session.rollback()
    db.session.remove()
    _user_stack.pop()

@app.route("/current_user")
def create_user():
    d = {
        "id": current_user.id,
        "name": current_user.name,
        "email": current_user.email,
    }
    return jsonify(d)


if __name__ == '__main__':
    app.run()
