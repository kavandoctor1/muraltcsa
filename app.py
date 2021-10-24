
# A very simple Flask Hello World app for you to get started with...
import sys
from flask import *
# import smtplib
# import time
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
# from email.mime.base import MIMEBase

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

# @app.route('/book')
# def book():
#     return render_template('book.html')

# @app.route('/download')
# def downloadFile ():
#     path = "static/Olympiad_Combinatorics.pdf"
#     x = int(open('/home/pranavsriram/mysite/downloadcounter.txt','r').read().strip())
#     open('/home/pranavsriram/mysite/downloadcounter.txt','w').write(str(x+1))
#     print(x,x+1)
#     return send_file(path, as_attachment=True)

# @app.route('/contact',methods=['POST'])
# def contact():
#     print(request.data,file=sys.stderr)
#     name = request.form.get('Name')
#     email = request.form.get('Email')
#     message = request.form.get('Message')
#     print(name,email,message,file=sys.stderr)
#     title = f'{name} sent you a message'
#     body = f'Message from {name}, with email address {email}: \n\n' + message
#     receiver = 'kavandoctor@gmail.com'
#     server = smtplib.SMTP('smtp.googlemail.com',587)
#     server.starttls()
#     server.login('pranavwebsiteemailbot@gmail.com','pranavsriram1')
#     msg = MIMEMultipart()
#     msg['Subject'] = title
#     msg.attach(MIMEText(body,'plain'))
#     text = msg.as_string()
#     server.sendmail("meme",receiver, text)
#     server.quit()
#     return redirect('/')
import twill.commands as tw

@app.route('/find',methods=['POST'])
def contact():
    print(request.data,file=sys.stderr)
    user = request.form.get('username')
    password = request.form.get('password')
    # tw.follow('https://practiceit.cs.washington.edu/user/problems-solved')

    tw.go('http://practiceit.cs.washington.edu/login')

    tw.fv("1", "usernameoremail", user)
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
        l = [date,'Done: '+str(done),'Not Done: '+str(ndone)]
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
print(get_calendar())

