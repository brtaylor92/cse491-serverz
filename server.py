#!/usr/bin/env python
import random
import socket
import time
from urlparse import urlparse, parse_qs
import cgi
from StringIO import StringIO
import jinja2

def handle_connection(conn):
    # Start reading in data from the connection
    req = conn.recv(1)
    count = 0
    while req[-4:] != '\r\n\r\n':
        req += conn.recv(1)
    req, headers = req.split('\r\n',1)
    d = {}
    for line in headers.split('\r\n')[:-2]:
        k, v = line.split(': ', 1)
        d[k.lower()] = v

    # Parse out the path and related info
    path = urlparse(req.split(' ', 3)[1])

    # The dict of pages we know how to get to
    response = {'/' : 'index.html', \
              '/content' : 'content.html', \
              '/file' : 'file.html', \
              '/image' : 'image.html', \
              '/form' : 'form.html', \
              '/submit' : 'submit.html', \
             }

    # Basic connection information and set up templates
    loader = jinja2.FileSystemLoader('./templates')
    env = jinja2.Environment(loader=loader)
    retval = 'HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n'
    args = {}

    # Check if the request is get or post, set up the args
    if req.startswith('GET '):
        args = parse_qs(path[4])
    elif req.startswith('POST '):
        l = int(d['content-length'])
        data = ''
        while len(data) < l:
            data += conn.recv(1)
        e = {'REQUEST_METHOD' : 'POST'}
        d = cgi.FieldStorage(fp=StringIO(data), headers=args, environ=e)
        try:
            args = dict([(x, [d[x].value]) for x in d.keys()])
        except AttributeError:
            pass

    # Check if we got a path to an existing page
    try:
        # Load the appropriate template
        template = env.get_template(response[path[2]])
    except KeyError:
        args['path'] = path[2]
        retval = 'HTTP/1.0 404 Not Found\r\n'
        template = env.get_template('404.html')

    # Render the page
    print template
    retval += template.render(args)
    conn.send(retval)

    # Done here
    conn.close()

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