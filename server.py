#!/usr/bin/env python
import random
import socket
import time
import cgi
from StringIO import StringIO


def handle_connection(conn):
    # Start reading in data from the connection
    req = conn.recv(1)
    count = 0
    while req[-4:] != '\r\n\r\n':
        req += conn.recv(1)

    # Parse the headers we've received
    req, data = req.split('\r\n',1)
    headers = {}
    for line in data.split('\r\n')[:-2]:
        k, v = line.split(': ', 1)
        headers[k.lower()] = v

    # Parse out the path and related info
    path = urlparse(req.split(' ', 3)[1])

    # Check if the request is get or post, set up the args
    # args = parse_qs(path[4])
    # args = parse_qs(environ['QUERY_STRING'])

    if req.startswith('POST '):
        while len(content) < int(headers['content-length']):
            content += conn.recv(1)
    fs = cgi.FieldStorage(fp=StringIO(content), headers=headers, environ={'REQUEST_METHOD' : 'POST'})
    args.update(dict([(x, [fs[x].value]) for x in fs.keys()]))

def main():
    s = socket.socket()         # Create a socket object
    host = socket.getfqdn() # Get local machine name
    port = random.randint(8000, 9999)
    s.bind((host, port))        # Bind to the port

    print 'Starting server on', host, port
    print 'The Web server URL for this would be http://%s:%d/' % (host, port)

    s.listen(5)                 # Now wait for client connection.

    print 'Entering infinite loop; hit CTRL-C to exit'
    while True:
        # Establish connection with client.    
        c, (client_host, client_port) = s.accept()
        print 'Got connection from', client_host, client_port
        handle_connection(c)
        
# boilerplate
if __name__ == "__main__":
    main()