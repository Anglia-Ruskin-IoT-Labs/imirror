#!/usr/bin/python3
import os
import sys
# Change working directory of this scripts directory, if it is run from somewhere else
os.chdir(os.path.dirname(os.path.realpath(sys.argv[0])))

from server import flask
# server/__init__.py runs at this import

flask.run(host='0.0.0.0', port=5005, threaded = True, ssl_context=('certs/cert.pem', 'certs/key.pem'))
