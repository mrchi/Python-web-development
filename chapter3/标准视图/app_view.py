#!/usr/bin/env python3
# coding=utf-8

"""
标准视图继承自 flask.view.View，必须实现 dispatch_request 方法。
"""

from flask import Flask, request
from flask.views import View

app = Flask(__name__)


class MyView(View):
    methods = ["GET", "POST", "PUT"]

    def dispatch_request(self, name):
        if request.method == "GET":
            return "Hello, {}!".format(name)
        elif request.method == "POST":
            return "Create new user: {}".format(name)
        else:
            return "UNSUPPORTED"

# add_url_rule(rule, endpoint=None, view_func=None, provide_automatic_options=None, **options)
app.add_url_rule(
    "/users/<name>",
    endpoint="users",
    view_func=MyView.as_view("users"),
)


if __name__ == '__main__':
    app.run(debug=True)
