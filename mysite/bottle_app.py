# A very simple Bottle Hello World app for you to get started with...
from bottle import default_app, route, template, TEMPLATE_PATH, static_file, run

if __name__ == "__main__":
    TEMPLATE_PATH.append("mysite/")

@route('/')
def index():
    return template('simple.tpl')

@route('/data/<filename>')
def server_static(filename):
    return static_file(filename, root='./data')

@route('/css/<filename>')
def server_static(filename):
    return static_file(filename, root='./css')

@route('/logs/<filename>.log')
def server_static(filename):
    return static_file('{}.log'.format(filename), root='./logs', mimetype='text/plain')

@route('/logs/<filename>')
def server_static(filename):
    return static_file(filename, root='./logs')

@route('/pob/builds/<filename>')
def server_static(filename):
    return static_file(filename, root='./pob/builds')

application = default_app()

if __name__ == "__main__":
    run(host='localhost', port=8080, debug=True)