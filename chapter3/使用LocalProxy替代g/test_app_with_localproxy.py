# coding=utf-8

import tempfile
import os

import pytest
from app_with_localproxy import app

@pytest.fixture
def client():
    db_fd, app.config['DATABASE'] = tempfile.mkstemp()
    app.config['TESTING'] = True
    client = app.test_client()

    yield client

    os.close(db_fd)
    os.unlink(app.config['DATABASE'])

def test_local_proxy(client):
    d = {
        "id": 1,
        "name": "xiaoming",
        "email": "xiaoming@github.com",
    }
    rv = client.get("/current_user")
    assert rv.get_json() == d
