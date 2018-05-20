# coding=utf-8

import pytest

from unique_url import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    client = app.test_client()
    yield client

def test_page1(client):
    rv = client.get("/projects/")
    assert rv.status_code == 200
    # 定义有斜线 + 访问无斜线 = HTTP 301
    rv = client.get("/projects")
    assert rv.status_code == 301

def test_page2(client):
    rv = client.get("/about")
    assert rv.status_code == 200
    # 定义无斜线 + 访问有斜线 = HTTP 404
    rv = client.get("/about/")
    assert rv.status_code == 404
