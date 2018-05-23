# coding=utf-8

import tempfile
import os

import pytest
from app import app
from users import User

@pytest.fixture
def client():
    db_fd, app.config['DATABASE'] = tempfile.mkstemp()
    app.config['TESTING'] = True
    client = app.test_client()

    yield client

    os.close(db_fd)
    os.unlink(app.config['DATABASE'])

def test_hook_decorator(client):
    rv = client.get("/users")
    assert b"0<br>Xiaoming" in rv.data
    assert b"0<br>xiaoming" not in rv.data
    assert b"github.com" in rv.data

def test_app_errorhandler(client):
    rv = client.get("/")
    assert {"msg": "page not found"} == rv.get_json()
