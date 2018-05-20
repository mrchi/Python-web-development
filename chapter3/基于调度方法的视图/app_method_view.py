#!/usr/bin/env python3
# coding=utf-8

"""
flask.view.MethodView 对每个 HTTP 方法执行不同的函数，对 RESTFul API 特别有用。类似
Tornado 的路由组织形式。

对视图的装饰有两种方法：
- 通过装饰 as_view 的返回值；
- 在继承 MethodView 的类中添加 decorators 属性。
"""

from flask import Flask, jsonify
from flask.views import MethodView

app = Flask(__name__)

def is_you(func):
    def wrapper(*args, **kw):
        if kw.get("name") == "you":
            return "love you"
        return func(*args, **kw)
    return wrapper


class UserAPI(MethodView):
    decorators = [is_you]

    def get(self, name):
        return "Hello, {}!".format(name)

    def post(self, name):
        return "Create new user: {}".format(name)

    def put(self, name):
        return "UNSUPPORTED"

app.add_url_rule(
    "/users/<name>",
    endpoint="users",
    view_func=UserAPI.as_view("userview")
)


if __name__ == '__main__':
    app.run(debug=True)
