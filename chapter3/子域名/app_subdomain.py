#!/usr/bin/env python3
# coding=utf-8

"""
通过子域名访问，使用 subdomain 实现。
"""

from flask import Flask, g, jsonify

app = Flask(__name__)
app.config["SERVER_NAME"] = "example.com:5000"

@app.url_value_preprocessor
def get_site(endpoint, values):
    g.site = values.pop("subdomain")

@app.route("/users/<name>", subdomain="<subdomain>")
def index(name):
    return jsonify(dict(sub_domain=g.site, name=name))


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000, debug=True)
