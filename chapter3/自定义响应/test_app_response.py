# coding=utf-8

import pytest

from app_response import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    client = app.test_client()
    yield client

def test_json_response(client):
    rv = client.get("/")
    assert rv.get_json() == {"message": "Hello, world!"}

def test_custom_headers_json_response(client):
    rv = client.get("/custom_headers")
    assert rv.get_json() == {"message": "Hello, world!"}
    assert rv.headers.get("X-Request-Id", type=int) == 100
    assert rv.status_code == 201
