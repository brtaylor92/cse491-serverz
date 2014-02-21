# encoding: utf-8

import jinja2
from urlparse import parse_qs
import cgi

def app(environ, start_response):
    """A simple WSGI application which serves several pages 
        and handles form data"""

    # The dict of pages we know how to serve, and their corresponding templates
    response = {
                '/'        : 'index.html',   \
                '/content' : 'content.html', \
                '/file'    : 'file.html',    \
                '/image'   : 'image.html',   \
                '/form'    : 'form.html',    \
                '/submit'  : 'submit.html',  \
                '404'      : '404.html',     \
               }

    # Basic connection information and set up templates
    loader = jinja2.FileSystemLoader('./templates')
    env = jinja2.Environment(loader=loader)
    response_headers = [('Content-type', 'text/html; charset="UTF-8"')]

    # Check if we got a path to an existing page
    if environ['PATH_INFO'] in response:
        # If we have that page, serve it with a 200 OK
        status = '200 OK'
        template = env.get_template(response[environ['PATH_INFO']])
    else:
        # If we did not, redirect to the 404 page, with appropriate status
        status = '404 Not Found'
        template = env.get_template(response['404'])

    # Set up template arguments from GET requests
    qs = parse_qs(environ['QUERY_STRING']).iteritems()
    # Flatten the list we get from parse_qs; just assume we want the 0th for now
    args = {key : val[0] for key, val in qs}
    # Add the path to the args; we'll use this for page titles and 404s
    args['path'] = environ['PATH_INFO']

    # Grab POST args if there are any
    if environ['REQUEST_METHOD'] == 'POST':
        # Re-parse the headers into a format field storage can use
        # Dashes instead of underscores, all lowercased
        headers = { 
                    key[5:].lower().replace('_','-') : val \
                    for key, val in environ.iteritems() \
                    if(key.startswith('HTTP'))
                  }
        # Pull in the non-HTTP variables that field storage needs manually
        headers['content-type'] = environ['CONTENT_TYPE']
        headers['content-length'] = environ['CONTENT_LENGTH']
        # Create a field storage to process POST args
        fs = cgi.FieldStorage(fp=environ['wsgi.input'], \
                                headers=headers, environ=environ)
        # Add these new args to the existing set
        args.update({key : fs[key].value for key in fs.keys()})

    # Get all the arguments in unicode form for Jinja
    args = {
            key.decode('utf-8') : val.decode('utf-8') \
            for key, val in args.iteritems()
           }
    
    # Return the page and status code
    # Page is first encoded to bytes from unicode for compatibility
    start_response(status, response_headers)
    return [template.render(args).encode('utf-8')]

def make_app():
    """Wrapper function; returns the app function above to a WSGI server"""
    return app
