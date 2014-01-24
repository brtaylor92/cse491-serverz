#!/usr/bin/env python
import random
import socket
import time

def handle_get(conn, path):
    response = {'/' : 'HTTP/1.0 200 OK\r\n' + \
                        'Content-type: text/html\r\n\r\n' + \
                        '<html>\r\n\t<body>\r\n\t\t' + \
                        '<h1>Hello, world.</h1>\r\n\t\t' + \
                        'This is brtaylor92\'s Web server.<br />\r\n\t\t' + \
                        '<a href=\'/content\'>Content</a><br />\r\n\t\t' + \
                        '<a href=\'/file\'>Files</a><br />\r\n\t\t' + \
                        '<a href=\'/image\'>Images</a><br />\r\n\t' + \
                        '</body>\r\n</html>', \
                 '/content' : 'HTTP/1.0 200 OK\r\n' + \
                              'Content-type: text/html\r\n\r\n' + \
                              '<html>\r\n\t<body>\r\n\t\t' + \
                              '<h1>Content Page</h1>\r\n\t\t' + \
                              'Content goes here, once there is any :)\r\n\t' + \
                              '</body>\r\n</html>', \
                 '/file' : 'HTTP/1.0 200 OK\r\n' + \
                           'Content-type: text/html\r\n\r\n' + \
                           '<html>\r\n\t<body>\r\n\t\t' + \
                           '<h1>File Page</h1>\r\n\t\t' + \
                           'Files go here, once there are any :)\r\n\t' + \
                           '</body>\r\n</html>', \
                 '/image' : 'HTTP/1.0 200 OK\r\n' + \
                            'Content-type: text/html\r\n\r\n' + \
                            '<html>\r\n\t<body>\r\n\t\t' + \
                            '<h1>Image Page</h1>\r\n\t\t' + \
                            'Images go here, once there are any :)\r\n\t' +\
                            '</body>\r\n</html>'
                }
    try:
        conn.send(response[path])
    except:
        # Page we don't have...
        conn.send('HTTP/1.0 404 Not Found\r\n')
        conn.send('Content-type: text/html\r\n\r\n')
        conn.send('<html>\r\n\t<body>\r\n\t\t')
        conn.send('<h1>Oops! Something went wrong...</h1>\r\n\t\t')
        conn.send('We couldn\'t find that page\r\n\t')
        conn.send('</body>\n</html>')

def handle_post(conn):
    conn.send('HTTP/1.0 200 OK\r\n\r\n')
    conn.send('Hello World')

def handle_connection(conn):
    req = conn.recv(1000)
    if req[0:4] == 'GET ':
        try:
            path = req.split(' ', 3)[1]
            handle_get(conn, path)
        except IndexError:
            handle_get(conn, '/404')
    elif req[0:5] == 'POST ':
        handle_post(conn)
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