import server

class FakeConnection(object):
    """
    A fake connection class that mimics a real TCP socket for the purpose
    of testing socket I/O.
    """
    def __init__(self, to_recv):
        self.to_recv = to_recv
        self.sent = ""
        self.is_closed = False

    def recv(self, n):
        if n > len(self.to_recv):
            r = self.to_recv
            self.to_recv = ""
            return r
            
        r, self.to_recv = self.to_recv[:n], self.to_recv[n:]
        return r

    def send(self, s):
        self.sent += s

    def close(self):
        self.is_closed = True

# Test a basic GET call.

def test_handle_connection_slash():
    conn = FakeConnection("GET / HTTP/1.0\r\n\r\n")
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/html\r\n' + \
                      '\r\n' + \
                      '<html>\r\n\t<body>\r\n\t\t' + \
                      '<h1>Hello, world.</h1>\r\n\t\t' + \
                      'This is brtaylor92\'s Web server.<br />\r\n\t\t' + \
                      '<a href=\'/content\'>Content</a><br />\r\n\t\t' + \
                      '<a href=\'/file\'>Files</a><br />\r\n\t\t' + \
                      '<a href=\'/image\'>Images</a><br />\r\n\t' + \
                      '</body>\r\n</html>'

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_handle_connection_content():
    conn = FakeConnection("GET /content HTTP/1.0\r\n\r\n")
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/html\r\n' + \
                      '\r\n' + \
                      '<html>\r\n\t<body>\r\n\t\t' + \
                      '<h1>Content Page</h1>\r\n\t\t' + \
                      'Content goes here, once there is any :)\r\n\t' + \
                      '</body>\r\n</html>'

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_handle_connection_file():
    conn = FakeConnection("GET /file HTTP/1.0\r\n\r\n")
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/html\r\n' + \
                      '\r\n' + \
                      '<html>\r\n\t<body>\r\n\t\t' + \
                      '<h1>File Page</h1>\r\n\t\t' + \
                      'Files go here, once there are any :)\r\n\t' + \
                      '</body>\r\n</html>'

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_handle_connection_image():
    conn = FakeConnection("GET /image HTTP/1.0\r\n\r\n")
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/html\r\n' + \
                      '\r\n' + \
                      '<html>\r\n\t<body>\r\n\t\t' + \
                      '<h1>Image Page</h1>\r\n\t\t' + \
                      'Images go here, once there are any :)\r\n\t' + \
                      '</body>\r\n</html>'

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_post():
    conn = FakeConnection("POST / HTTP/1.1\r\n\r\n")
    expected_return = '200\r\n' + \
                      'Hello World'
