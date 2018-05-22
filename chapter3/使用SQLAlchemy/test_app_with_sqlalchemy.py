# coding=utf-8

import tempfile
import os

import pytest
from app_with_sqlalchemy import app, db
from users import User

@pytest.fixture
def client():
    db_fd, app.config['DATABASE'] = tempfile.mkstemp()
    app.config['TESTING'] = True
    client = app.test_client()

    with app.app_context():
        db.drop_all()
        db.create_all()

    yield client

    os.close(db_fd)
    os.unlink(app.config['DATABASE'])

def test_sqlalchemy(client):
    rv = client.post("/users", json=dict(name="invoker"))
    with app.app_context():
        name = db.session.query(User.name) \
                        .filter_by(id=rv.get_json()["id"]) \
                        .scalar()
    assert name == "invoker"
