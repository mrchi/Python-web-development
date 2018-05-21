# coding=utf-8

import os
import pytest
from app_cli import app, hello_command

@pytest.fixture
def runner():
    os.environ["FLASK_APP"] = "app_cli.py"
    runner = app.test_cli_runner()
    yield runner
    os.environ["FLASK_APP"] = ""

def test_hello_params(runner):
    context = hello_command.make_context("hello", ["--name", "flask"])
    assert context.params["name"] == "FLASK"

def test_hello(runner):
    result = runner.invoke(args=["hello"])
    assert "WORLD" in result.output

