#!/usr/bin/python
from app import server
server.run(host='0.0.0.0', port=5005, threaded = True, ssl_context=('certs/cert.pem', 'certs/key.pem'))
