#!/usr/bin/env python
import random
import socket
import time
from urlparse import urlparse, parse_qs
import cgi
import StringIO
import re
import jinja2

def handle_get(conn, path):
    args = parse_qs(urlparse(path)[4])
    response = {'/' : 'index.html', \
              '/content' : 'content.html', \
              '/file' : 'file.html', \
              '/image' : 'image.html', \
              '/form' : 'form.html', \
              '/submit' : 'submit.html', \
             }
    loader = jinja2.FileSystemLoader('./templates')
    env = jinja2.Environment(loader=loader)
    retval = 'HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n'
    try:
        path = response[urlparse(path)[2]]
    except KeyError:
        args['path'] = path
        retval = 'HTTP/1.0 404 Not Found\r\n'
        path = '404.html'
    template = env.get_template(path)
    retval += template.render(args)
    conn.send(retval)

def handle_post(conn, path, **kwargs):
    arg0 = StringIO.StringIO(kwargs['data'])
    kwargs.pop('data')

    e = {}
    e['REQUEST_METHOD'] = 'POST'

    data = cgi.FieldStorage(fp=arg0, headers=kwargs, environ=e)

    args = dict([(x, [data[x].value]) for x in data.keys()])
    response = {'/submit' : 'submit.html',}
    loader = jinja2.FileSystemLoader('./templates')
    env = jinja2.Environment(loader=loader)
    retval = 'HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n'
    try:
        path = response[urlparse(path)[2]]
    except KeyError:
        args['path'] = path
        retval = 'HTTP/1.0 404 Not Found\r\n'
        path = '404.html'
    template = env.get_template(path)
    retval += template.render(args)
    conn.send(retval)

def handle_connection(conn):
    req = conn.recv(1)
    count = 0
    while req[-4:] != '\r\n\r\n':
        req += conn.recv(1)
    req, headers = req.split('\r\n',1)
    d = {}
    for line in headers.split('\r\n')[:-2]:
        k, v = line.split(': ', 1)
        d[k.lower()] = v
    if req.startswith('GET '):
        path = req.split(' ', 3)[1]
        handle_get(conn, path)
    elif req.startswith('POST '):
        path = req.split(' ', 3)[1]
        l = int(d['content-length'])
        data = ''
        while len(data) < l:
            data += conn.recv(1)
        d['data'] = data
        handle_post(conn, path, **d)
    else:
        print req
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