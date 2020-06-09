

def application(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/html')])
    print(environ["PATH_INFO"])
    body = '<h1>Hello, %s!</h1>' % (environ['PATH_INFO'][1:] or 'web')
    return [body.encode('utf-8')]