#!/usr/bin/env python3
# coding=utf-8

"""
实现一个自定义的响应类，当在视图函数中返回 dict 类型数据时，自动返回 JSON 格式的响应。

继承自 flask.wrappers.Response 类，实现类方法 force_type，以用于强制转换视图函数的返
回值为Response对象。参考 P38 响应转换逻辑第四条。
"""

from flask import Flask, jsonify
from flask.wrappers import Response

app = Flask(__name__)


class JSONResponse(Response):
    @classmethod
    def force_type(cls, rv, environ=None):
        if isinstance(rv, dict):
            rv = jsonify(rv)
        return super(JSONResponse, cls).force_type(rv, environ)

app.response_class = JSONResponse

@app.route("/")
def hello():
    return {"message": "Hello, world!"}

@app.route("/custom_headers")
def custom_headers():
    return {"message": "Hello, world!"}, 201, [("X-Request-Id", "100")]


if __name__ == '__main__':
    app.run(debug=True)
