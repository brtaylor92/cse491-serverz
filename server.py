#!/usr/bin/env python
import random
import socket
import time
from urlparse import urlparse, parse_qs
import cgi
import StringIO
import re
import jinja2

def index(conn, **kwargs):
    loader = jinja2.FileSystemLoader('./templates')
    env = jinja2.Environment(loader=loader)
    template = env.get_template('index.html')
    retval = 'HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n' + \
              template.render(kwargs)
    return  retval

def file(conn, **kwargs):
    return  'HTTP/1.0 200 OK\r\n' + \
            'Content-type: text/html\r\n\r\n' + \
            '<html>\r\n\t<body>\r\n\t\t' + \
            '<h1>File Page</h1>\r\n\t\t' + \
            'Files go here, once there are any :)\r\n\t' + \
            '</body>\r\n</html>'

def content(conn, **kwargs):
    return  'HTTP/1.0 200 OK\r\n' + \
            'Content-type: text/html\r\n\r\n' + \
            '<html>\r\n\t<body>\r\n\t\t' + \
            '<h1>Content Page</h1>\r\n\t\t' + \
            'Content goes here, once there is any :)\r\n\t' + \
            '</body>\r\n</html>'

def image(conn, **kwargs):
    return  'HTTP/1.0 200 OK\r\n' + \
            'Content-type: text/html\r\n\r\n' + \
            '<html>\r\n\t<body>\r\n\t\t' + \
            '<h1>Image Page</h1>\r\n\t\t' + \
            'Images go here, once there are any :)\r\n\t' + \
            '</body>\r\n</html>'

def form(conn, **kwargs):
    return  'HTTP/1.0 200 OK\r\n' + \
            'Content-type: text/html\r\n\r\n' + \
            '<html>\r\n\t<body>\r\n\t\t' + \
            '<form action=\'/submit\' method=\'POST\'>\r\n\t\t' + \
            '<input type=\'text\' name=\'firstname\'>\r\n\t\t' + \
            '<input type=\'text\' name=\'lastname\'>\r\n\t\t' + \
            '<input type=\'submit\' name=\'submit\'>\r\n\t\t' + \
            '</form>\r\n\t' + \
            '</body>\r\n</html>'

def submit(conn, **kwargs):
    fname = ''
    lname = ''
    try:
        fname = kwargs['firstname'][0]
    except KeyError:
        pass
    try:
        lname = kwargs['lastname'][0]
    except KeyError:
        pass

    return  'HTTP/1.0 200 OK\r\n' + \
            'Content-type: text/html\r\n\r\n' + \
            '<html>\r\n\t<body>\r\n\t\t' + \
            '<h1>Hello {0} {1}'.format(fname, lname) + \
            '</h1>\r\n\t' + \
            '</body>\r\n</html>'

def psubmit(conn, **kwargs):
    arg0 = StringIO.StringIO(kwargs['data'])
    kwargs = dict([(k.lower(), v) for k,v in kwargs.iteritems()])
    kwargs.pop('data')

    e = {}
    e['REQUEST_METHOD'] = 'POST'

    data = cgi.FieldStorage(fp=arg0, headers=kwargs, environ=e)

    fname = data['firstname'].value
    lname = data['lastname'].value

    return  'HTTP/1.0 200 OK\r\n' + \
            'Content-type: text/html\r\n\r\n' + \
            '<html>\r\n\t<body>\r\n\t\t' + \
            '<h1>Hello {0} {1}'.format(fname, lname) + \
            '</h1>\r\n\t' + \
            '</body>\r\n</html>'

def fof(conn, **kwargs):
    # Page we don't have...
    return  'HTTP/1.0 404 Not Found\r\n' + \
            'Content-type: text/html\r\n\r\n' + \
            '<html>\r\n\t<body>\r\n\t\t' + \
            '<h1>Oops! Something went wrong...</h1>\r\n\t\t' + \
            'We couldn\'t find that page\r\n\t' + \
            '</body>\n</html>'

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
    try:
        path = response[urlparse(path)[2]]
    except KeyError:
        path = '404.html'
    template = env.get_template(path)
    retval = 'HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n' + \
              template.render(args)
    conn.send(retval)

def handle_post(conn, path, **kwargs):
    response = {'/submit' : psubmit,}
    try:
        conn.send(response[path](conn, **kwargs))
    except KeyError:
        conn.send(fof(conn, **kwargs))

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