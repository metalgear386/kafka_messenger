#!/usr/bin/python3
"""Test msg
"""
import receiver as rc
import getpass
import logging
import os
import sys
import time
import subprocess
import message_sender as ms
from flask import Flask
import flask

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/test")
def check_messages():
    return rc.check_for_msgs()


@app.route('/yield')
def index():
    def inner():
        while True:
            proc = rc.check_for_msgs()
            return proc
            #for line in proc:
            #    time.sleep(0.1)                           # Don't need this just shows the text streaming
            #    yield str(proc + str('<br/>\n'))
    return flask.Response(inner(), mimetype='text/html') 

if __name__ == "__main__":
    app.run(host= '0.0.0.0')
