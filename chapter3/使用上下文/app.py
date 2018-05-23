#!/usr/bin/env python3
# coding=utf-8

import random

from flask import Flask, request, jsonify, g, render_template


from ext import db
from users import User

app = Flask(__name__, template_folder=".")
app.config.from_object("config")
db.init_app(app)


def get_current_user():
    users = User.query.all()
    return random.choice(users)


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
    g.user = get_current_user()


@app.teardown_appcontext
def teardown(exc=None):
    if exc is None:
        db.session.commit()
    else:
        db.session.rollback()
    db.session.remove()
    g.user = None


@app.context_processor
def template_extras():
    return {"enumerate": enumerate, "current_user": g.user}


@app.template_filter("capitalize")
def reverse_filter(s):
    return s.capitalize()


@app.errorhandler(404)
def page_not_found(error):
    return jsonify(dict(msg="page not found")), 404


@app.route("/users")
def create_user():
    users = User.query.all()
    return render_template("users.html", users=users)


if __name__ == '__main__':
    app.run()
