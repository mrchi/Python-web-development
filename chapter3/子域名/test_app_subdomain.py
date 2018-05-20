# coding=utf-8

import pytest

from app_subdomain import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    client = app.test_client()
    yield client

def test_app_subdomain(client):
    # 貌似无论什么域名请求的都是 app 的路由
    rv = client.get("http://test.example.com:5000/users/flask")
    assert rv.get_json() == dict(sub_domain="test", name="flask")
