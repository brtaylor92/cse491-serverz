#!/usr/bin/env python
from wsgiref.validate import validator
from app import make_app
from wsgiref.simple_server import make_server
import socket
import random


def main():
	wsgi_app = make_app()
	val_app = validator(wsgi_app)
	host = socket.getfqdn() # Get local machine name
	port = random.randint(8000, 9999)
	httpd = make_server('', port, wsgi_app)
	print "Serving at http://%s:%d/..." % (host, port,)
	httpd.serve_forever()

if __name__ == "__main__":
	main()