import json,os
from bottle import default_app, route, template, TEMPLATE_PATH, static_file, run
if __name__ == "__main__":
    TEMPLATE_PATH.append("mysite/")

mysite = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

@route('/')
def index():
    accountdb = f'{mysite}/accountdb.json'
    accounts = {}
    if os.path.exists(accountdb):
        with open(accountdb) as json_file:
            accounts = json.load(json_file)
            return template(f'index.tpl',{"accounts": accounts})

@route('/data/<filename>')
def server_static(filename):
    return static_file(filename, root=f'{mysite}/data')

@route('/css/<filename>')
def server_static(filename):
    return static_file(filename, root=f'{mysite}/css')

@route('/logs/<filename>.log')
def server_static(filename):
    return static_file('{}.log'.format(filename), root=f'{mysite}/logs', mimetype='text/plain')

@route('/logs/<filename>')
def server_static(filename):
    return static_file(filename, root=f'{mysite}/logs')

@route('/pob/builds/<filename>')
def server_static(filename):
    return static_file(filename, root=f'{mysite}/pob/builds')

@route('/console')
def server_static():
    return static_file("scan_all.log", root=f'{mysite}', mimetype='text/plain')

application = default_app()

if __name__ == "__main__":
    run(host='localhost', port=8080, debug=True)