import jinja2
from urlparse import urlparse, parse_qs
import cgi

def app(environ, start_response):
    # The dict of pages we know how to get to
    response = {
                '/'        : 'index.html',   \
                '/content' : 'content.html', \
                '/file'    : 'file.html',    \
                '/image'   : 'image.html',   \
                '/form'    : 'form.html',    \
                '/submit'  : 'submit.html',  \
               }

    # Basic connection information and set up templates
    loader = jinja2.FileSystemLoader('./templates')
    env = jinja2.Environment(loader=loader)
    response_headers = [('Content-type', 'text/html')]

    # Check if we got a path to an existing page
    if environ['PATH_INFO'] in response:
        status = '200 OK'
        template = env.get_template(response[environ['PATH_INFO']])
    else:
        status = '404 Not Found'
        template = env.get_template('404.html')

    # Set up template arguments
    args = parse_qs(environ['QUERY_STRING'])
    args['path'] = environ['PATH_INFO']

    if environ['REQUEST_METHOD'] == 'POST':
        # Grab POST args if there are any
        fs = cgi.FieldStorage(fp=environ['wsgi.input'], headers={'content-type':environ['CONTENT_TYPE']}, environ=environ)
        args.update(dict([(x, [fs[x].value]) for x in fs.keys()]))

    print args
    # Return the page
    start_response(status, response_headers)
    return str(template.render(args))

def make_app():
    return app