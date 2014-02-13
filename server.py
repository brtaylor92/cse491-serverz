#!/usr/bin/env python
import random
import socket
import time
from urlparse import urlparse
from StringIO import StringIO
from app import make_app

def handle_connection(conn):
    """Takes a socket connection, and serves a WSGI app over it.
        Connection is closed when app is served."""
    
    # Start reading in data from the connection
    req = conn.recv(1)
    count = 0
    env = {}
    while req[-4:] != '\r\n\r\n':
        req += conn.recv(1)

    # Parse the headers we've received
    req, data = req.split('\r\n',1)
    headers = {}
    for line in data.split('\r\n')[:-2]:
        k, v = line.split(': ', 1)
        headers[k.lower()] = v

    # Parse the path and related env info
    info = urlparse(req.split(' ', 3)[1])
    env['REQUEST_METHOD'] = 'GET'
    env['PATH_INFO'] = info[2]
    env['QUERY_STRING'] = info[4]
    env['CONTENT_TYPE'] = 'text/html'
    env['CONTENT_LENGTH'] = 0

    # Start response function for WSGI interface
    def start_response(status, response_headers):
        """Send the initial HTTP header, with status code 
            and any other provided headers"""
        
        # Send HTTP status
        conn.send('HTTP/1.0 ')
        conn.send(status)
        conn.send('\r\n')

        # Send the response headers
        for pair in response_headers:
            key, header = pair
            conn.send(key + ': ' + header + '\r\n')
        conn.send('\r\n')
    
    # If we received a POST request, collect the rest of the data
    content = ''
    if req.startswith('POST '):
        # Set up extra env variables
        env['REQUEST_METHOD'] = 'POST'
        env['CONTENT_LENGTH'] = headers['content-length']
        env['CONTENT_TYPE'] = headers['content-type']
        # Continue receiving content up to content-length
        while len(content) < int(headers['content-length']):
            content += conn.recv(1)
    
    # Set up a StringIO to mimic stdin for the FieldStorage in the app
    env['wsgi.input'] = StringIO(content)
    
    # Get the application
    appl = make_app()
    result = appl(env, start_response)

    # Serve the processed data
    for data in result:
        conn.send(data)

    # Close the connection; we're done here
    conn.close()
    

def main():
    """Waits for a connection, then serves a WSGI app using handle_connection"""
    # Create a socket object
    s = socket.socket()
    
    # Get local machine name (fully qualified domain name)
    host = socket.getfqdn()

    # Bind to a (random) port
    port = random.randint(8000, 9999)
    s.bind((host, port))

    print 'Starting server on', host, port
    print 'The Web server URL for this would be http://%s:%d/' % (host, port)

    # Now wait for client connection.
    s.listen(5)

    print 'Entering infinite loop; hit CTRL-C to exit'
    while True:
        # Establish connection with client.    
        c, (client_host, client_port) = s.accept()
        print 'Got connection from', client_host, client_port
        handle_connection(c)
        
# boilerplate
if __name__ == "__main__":
    main()