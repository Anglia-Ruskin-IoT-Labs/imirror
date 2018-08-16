#!/usr/bin/python3
from server import flask
# server/__init__.py runs at this import

flask.run(host='0.0.0.0', port=5005, threaded = True, ssl_context="adhoc")
