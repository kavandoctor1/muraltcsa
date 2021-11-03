import sys
from flask import *
import flask
import flask_login
import os
app = Flask(__name__)
login_manager = flask_login.LoginManager()
app.secret_key = os.urandom(24)
login_manager.init_app(app)
def load_users():
    USERS = eval(open('users.txt','r').read())
    return USERS
def save_users(USERS):
    open('users.txt','w').write(str(USERS))
class User(flask_login.UserMixin):
    pass
@login_manager.user_loader
def user_loader(username):
    USERS = load_users()
    if username not in USERS:
        return
    user = User()
    user.id = username
    return user

@app.route('/login', methods=['GET', 'POST'])
def login():
    if flask.request.method == 'GET':
        return render_template('login.html',incorrect = False)

    username = flask.request.form['username']
    USERS = load_users()
    if username in USERS and flask.request.form['password'] == USERS[username]['password']:
        load_users()
        user = User()
        user.id = username
        flask_login.login_user(user)
        return flask.redirect('/find')
    else:
        return render_template('login.html',incorrect=True)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if flask.request.method == 'GET':
        return render_template('register.html',incorrect = False,exists=False)

    username = flask.request.form['username']
    password = flask.request.form['password']
    cbusername = flask.request.form['cbusername']
    cbpassword = flask.request.form['cbpassword']
    print(cbusername,cbpassword)
    USERS = load_users()
    if username in USERS:
        return render_template('register.html',incorrect=False,exists=True)
    if not isvalid(cbusername,cbpassword):
        return render_template('register.html',incorrect=True,exists=False)
    load_users()
    USERS[username] = {"password":password,"cbusername":cbusername,"cbpassword":cbpassword}
    save_users(USERS)
    return flask.redirect('/login')
    

@app.route('/logout')
def logout():
    flask_login.logout_user()
    return 'Logged out'

@login_manager.unauthorized_handler
def unauthorized_handler():
    return redirect('/login')

@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    USERS = load_users()
    if username not in USERS:
        return
    user = User()
    user.id = username
    return user


@app.route('/')
def home():
    return render_template('index.html')

import twill.commands as tw

@app.route('/find',methods=['GET'])
@flask_login.login_required
def exercises():
    print(request.data,file=sys.stderr)
    USERS = load_users()
    username = flask_login.current_user.id
    cbusername = USERS[username]['cbusername']
    cbpassword = USERS[username]['cbpassword']
    # tw.follow('https://practiceit.cs.washington.edu/user/problems-solved')

    tw.go('http://practiceit.cs.washington.edu/login')

    tw.fv("1", "usernameoremail", cbusername)
    tw.fv("1", "password", cbpassword)
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
def isvalid(username,password):
    tw.reset_browser()
    tw.go('http://practiceit.cs.washington.edu/login')

    tw.fv("1", "usernameoremail", username)
    tw.fv("1", "password", password)
    tw.submit('login')
    tw.go('https://practiceit.cs.washington.edu/')
    s = tw.show()
    tw.reset_browser()
    return 'Start' in s
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

