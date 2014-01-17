#!/usr/bin/env python
import random
import socket
import time


def handle_connection(conn):
    print conn.recv(1000)
    print 'Got connection from', client_host, client_port
    conn.send('HTTP/1.0 200 OK\r\n')
    conn.send('Content-Type: text/html\r\n\r\n')
    conn.send("<h1>Hello, world</h1> this is brtaylor92's Web server\r\n")
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
        handle_connection(c)

#boilerplate
if __name__ == "__main__":
    main()