#!/usr/bin/env python3
# coding=utf-8

import logging
from logging.handlers import RotatingFileHandler

from flask import Flask, jsonify
from flask_sqlalchemy import get_debug_queries, SQLAlchemy

from consts import DB_URI

app = Flask(__name__)
app.config["DEBUG"] = True
app.config["DATABASE_QUERY_TIMEOUT"] = 0.0001
app.config["SQLALCHEMY_RECORD_QUERIES"] = True
app.config["SQLALCHEMY_DATABASE_URI"] = DB_URI


db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50))

    def __init__(self, name):
        self.name = name


db.init_app(app)

with app.app_context():
    db.drop_all()
    db.create_all()

formatter = logging.Formatter(
    "[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s"
)
handler = RotatingFileHandler("slow_query.log", maxBytes=10000, backupCount=10)
handler.setLevel(logging.WARN)
handler.setFormatter(formatter)
app.logger.addHandler(handler)

@app.after_request
def after_request(response):
    for query in get_debug_queries():
        if query.duration >= app.config["DATABASE_QUERY_TIMEOUT"]:
            app.logger.warn(
                f"Context:{query.context}\n"
                f"SLOW QUERY: {query.statement}\n"
                f"Parameters: {query.parameters}\n"
                f"Duration: {query.duration}\n"
            )
    return response

@app.route("/users/<int:id>")
def get_users(id):
    user = db.session.query(User).filter_by(id=id).one_or_none()
    return jsonify({"id": user.id if user else 0})


if __name__ == '__main__':
    app.run()
