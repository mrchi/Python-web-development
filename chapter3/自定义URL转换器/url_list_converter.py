#!/usr/bin/env python3
# coding=utf-8

"""
自定义一个 URL 转换器，实现类似 Reddit 的功能——用加号（+）隔开各个社区的名字，方便同时查看来自
多个社区的帖子。如“http://reddit.com/r/flask+lisp”，用于同时查看 flask 和 lisp 两个社区
的帖子。

自定义 URL 转换器继承自 werkzeug.routing.BaseConverter，
需要实现 to_python 和 to_url 两个方法。
"""

import urllib.parse

from flask import Flask
from werkzeug.routing import BaseConverter

app = Flask(__name__)


class ListConverer(BaseConverter):
    def __init__(self, url_map, separator="+"):
        super(ListConverer, self).__init__(url_map)
        self.separator = urllib.parse.unquote(separator)

    def to_python(self, value):
        """将url转换为参数"""
        return value.split(self.separator)

    def to_url(self, values):
        """将参数转换为URL，比如 url_for"""
        return self.separator.join(
            super(ListConverer, self).to_url(value) for value in values
        )


app.url_map.converters["list"] = ListConverer


@app.route("/list1/<list:page_names>/")
def list1(page_names):
    return "Separator: {} {}".format("+", page_names)

@app.route("/list2/<list(separator='|'):page_names>/")
def list2(page_names):
    return "Separator: {} {}".format("|", page_names)


if __name__ == '__main__':
    app.run(debug=True)
