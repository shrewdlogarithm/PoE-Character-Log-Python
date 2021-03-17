import json,os
from bottle import default_app, route, template, TEMPLATE_PATH, static_file, run
if __name__ == "__main__":
    TEMPLATE_PATH.append("mysite/")

@route('/')
def index():
    if not os.path.exists("./mysite/index.html"):
        accountdb = "accountdb.json"
        accounts = {}
        if os.path.exists(accountdb):
            with open(accountdb) as json_file:
                accounts = json.load(json_file)
                return template('index.tpl',{"accounts": accounts})
    else:
        return static_file("index.html", root='./mysite')

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

@route('/console')
def server_static():
    return static_file("scan_all.log", root='.', mimetype='text/plain')

application = default_app()

if __name__ == "__main__":
    run(host='localhost', port=8080, debug=True)