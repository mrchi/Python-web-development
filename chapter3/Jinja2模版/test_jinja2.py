# coding=utf-8

import os
import datetime

import pytest
from jinja2 import Environment, FileSystemLoader

@pytest.fixture
def template():
    loader = FileSystemLoader(os.path.dirname(__file__))
    template = Environment(loader=loader).get_template("index.html")
    yield template

def test_extends(template):
    html = template.render(time=datetime.datetime.now())
    assert "description" in html                # super()从base模版继承而来
    assert "<title>Index</title>" in html       # 当前模版重写
    assert "<p>I'm not here.</p>" not in html   # base模版实现但被重写
    assert "<p>I'm footer.</p>" in html         # 当前模版没有实现该block，从base模版继承

def test_comment(template):
    html = template.render(time=datetime.datetime.now())
    assert "This is a comment" not in html

def test_include(template):
    html = template.render(time=datetime.datetime.now())
    assert "<h1>Content</h1>" in html

def test_marco(template):
    now = datetime.datetime.now()
    html = template.render(time=now)
    assert "Hello, world!" in html
    assert str(now.year) in html
