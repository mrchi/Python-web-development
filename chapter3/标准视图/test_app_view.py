# coding=utf-8

import pytest

from app_view import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    client = app.test_client()
    yield client

def test_app_view(client):
    url = "/users/python"
    assert client.get(url).data == b"Hello, python!"
    assert client.post(url).data == b"Create new user: python"
    assert client.put(url).data == b"UNSUPPORTED"
