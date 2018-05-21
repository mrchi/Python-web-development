#!/usr/bin/env python3
# coding=utf-8

import sys
import code
import click
from flask import Flask
from flask.cli import with_appcontext

try:
    import Ipython
    has_ipython = True
except ImportError:
    has_ipython = False

app = Flask(__name__)

def upper(ctx, param, value):
    if value is not None:
        return value.upper()

@app.cli.command("hello")
@click.option("--name", default="World", callback=upper)
def hello_command(name):
    click.echo(f"Hello, {name}!")

def plain_shell(user_ns, banner):
    sys.exit(code.interact(banner=banner, local=user_ns))

def ipython_shell(user_ns, banner):
    Ipython.embed(banner1=banner, user_ns=user_ns)

@app.cli.command("myshell", short_help="Runs a shell in the app context.")
@click.option("--plain", help="Use Plain Shell", is_flag=True)
@with_appcontext
def shell_command(plain):
    from flask.globals import _app_ctx_stack
    app = _app_ctx_stack.top.app
    banner = "Python {} on {}\n" \
            "App: {}{}\n" \
            "Instance: {}".format(
        sys.version,
        sys.platform,
        app.import_name,
        app.debug and " [debug]" or "",
        app.instance_path,
    )
    user_ns = app.make_shell_context()
    use_plain_shell = not has_ipython or plain
    if use_plain_shell:
        plain_shell(user_ns, banner)
    else:
        ipython_shell(user_ns, banner)
