#!/usr/bin/env python
import random
import socket
import time
from urlparse import urlparse, parse_qs

def index(conn, **kwargs):
    return  'HTTP/1.0 200 OK\r\n' + \
            'Content-type: text/html\r\n\r\n' + \
            '<html>\r\n\t<body>\r\n\t\t' + \
            '<h1>Hello, world.</h1>\r\n\t\t' + \
            'This is brtaylor92\'s Web server.<br />\r\n\t\t' + \
            '<a href=\'/content\'>Content</a><br />\r\n\t\t' + \
            '<a href=\'/file\'>Files</a><br />\r\n\t\t' + \
            '<a href=\'/image\'>Images</a><br />\r\n\t' + \
            '</body>\r\n</html>'

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
    response = {'/' : index, \
              '/content' : content, \
              '/file' : file, \
              '/image' : image, \
              '/form' : form, \
              '/submit' : submit, \
             }
    try:
        conn.send(response[urlparse(path)[2]](conn, **args))
    except KeyError:
        conn.send(fof(conn, **args))

def handle_post(conn, path, data):
    args = parse_qs(data)
    response = {'/submit' : psubmit,}
    try:
        conn.send(response[path](conn, **args))
    except KeyError:
        conn.send(fof(conn, **args))

def handle_connection(conn):
    req = conn.recv(1000)
    if req.startswith('GET '):
        try:
            path = req.split(' ', 3)[1]
        except IndexError:
            handle_get(conn, '/404')
        handle_get(conn, path)
    elif req.startswith('POST '):
        handle_post(conn, req.split(' ', 3)[1], req.split('\r\n\r\n')[1])
    else:
        print req[0:5]
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