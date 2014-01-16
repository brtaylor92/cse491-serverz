#!/usr/bin/env python
import random
import socket
import time

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
    #@Add c.recv() to ensure page loads
    print c.recv(1000)
    #send a response
    c.send('HTTP/1.0 200 OK\r\n')
    #@ added missing blank line
    c.send('Content-type: text/html\r\n\r\n')
    #@Add close h1 tag
    c.send('<h1>Hello, world.</h1>')
    c.send('This is ctb\'s Web server.')
    c.close()
