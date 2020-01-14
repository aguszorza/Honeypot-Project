#! /usr/bin/env python2

from bottle import route, run, template, request, app, redirect, static_file
from beaker.middleware import SessionMiddleware

session_opts = {
    'session.type': 'file',
    'session.cookie_expires': 300000,
    'session.data_dir': '/tmp/session',
    'session.auto': True,
    'session.key': "sessionid"
}

app = application = myapp = SessionMiddleware(app(), session_opts)

@route('/')
def root_page():
    session = request.environ.get('beaker.session')
    if ('log_in' in session and session['log_in'] == True):
        return template("welcome", name=session['login'])
    else:
        session['log_in'] = False
        redirect("/login")
        
@route('/login')
def authentication():
    username = request.params.get('username')
    password = request.params.get('password')
    if username is None:
        response = open("index.html").read()%("")
        return response
    if password is None:
        response = open("index.html").read()%(username)
        return response

    user = checkAuth(username, password)
    if user is not None:
        session = request.environ.get('beaker.session')
        session['log_in'] = True
        session['login'] = user
        redirect('/')
        return
        
    response = open("index.html").read()%(username)
    return response
    
@route('/logout')
def logout():
    session = request.environ.get('beaker.session')
    session.delete()
    redirect('/')
    
def checkAuth(username, password):
    if  (username == 'admin' and password == 'admin'):
        return username
    return None
    
if __name__ == '__main__':
    run (host='192.168.1.3', port=80, app=myapp)
    



    
            
        
