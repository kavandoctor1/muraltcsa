import sys
from flask import *
import flask
import flask_login
import os
app = Flask(__name__)

login_manager = flask_login.LoginManager()
app.secret_key = os.urandom(24)
login_manager.init_app(app)
users = {'kavandoctor': {'password': 'kavandoctor1'}}

class User(flask_login.UserMixin):
    pass
@login_manager.user_loader
def user_loader(email):
    if email not in users:
        return
    user = User()
    user.id = email
    return user

@app.route('/login', methods=['GET', 'POST'])
def login():
    if flask.request.method == 'GET':
        return render_template('login.html',incorrect = False)

    email = flask.request.form['email']
    if email in users and flask.request.form['password'] == users[email]['password']:
        user = User()
        user.id = email
        flask_login.login_user(user)
        return flask.redirect('/find')
    else:
        return render_template('login.html',incorrect=True)

@app.route('/logout')
def logout():
    flask_login.logout_user()
    return 'Logged out'

@login_manager.unauthorized_handler
def unauthorized_handler():
    return redirect('/login')

@login_manager.request_loader
def request_loader(request):
    email = request.form.get('email')
    if email not in users:
        return
    user = User()
    user.id = email
    return user


@app.route('/')
def home():
    return render_template('index.html')

import twill.commands as tw

@app.route('/find',methods=['GET'])
@flask_login.login_required
def contact():
    print(request.data,file=sys.stderr)
    username = flask_login.current_user.id
    password = users[username]['password']
    # tw.follow('https://practiceit.cs.washington.edu/user/problems-solved')

    tw.go('http://practiceit.cs.washington.edu/login')

    tw.fv("1", "usernameoremail", username)
    tw.fv("1", "password", password)
    tw.submit('login')
    tw.go('https://practiceit.cs.washington.edu/user/problems-solved')

    s = [l.split('</a>')[0][1:].split(':')[0] for l in tw.show().split('BJP4')[1:]][1::2] # completed exercises
    calendar = get_calendar()
    send =[]
    for date,due in calendar:
        done = []
        ndone = []
        for k in due: 
            if k in s:
                done.append(k)
            else:
                ndone.append(k)
        l = [date,done,ndone]
        send.append(l)
    print(send)
    tw.reset_browser()
    return render_template('exercises.html',send=send)

def get_calendar():
    l = open('calendar.txt','r').read().strip().split('\n\n')
    calendar = []
    for day in l:
        day = day.split('\n')
        date,day = day[0],day[1:]
        ex = []
        for row in day:
            start = 'Self-Check' if row.split()[0] == 'SC' else 'Exercise'
            for ch in row.split()[1].split(','):
                a,b = map(int,ch.split('.'))
                ex.append(f'{start} {a}.{b:02d}')
        calendar.append([date,ex])
    return calendar
# print(get_calendar())