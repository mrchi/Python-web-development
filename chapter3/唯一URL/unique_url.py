#!/usr/bin/env python3
# coding=utf-8

"""
唯一 URL 主张

定义路由有斜线结尾 + 访问路由无斜线结尾 => HTTP 301 永久重定向
定义路由无斜线结尾 + 访问路由有斜线结尾 => HTTP 404
"""

from flask import Flask

app = Flask(__name__)

@app.route("/projects/")
def projects():
    return "The project page"

@app.route("/about")
def about():
    return "The about page"


if __name__ == '__main__':
    app.run(debug=True)
