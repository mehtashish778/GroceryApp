from flask import request,render_template,redirect, url_for

from main import app
from main import get_db
from main import session
from models import *



@app.route('/signup', methods =['GET', 'POST'])
def signup():
    msg=''
    if request.method == 'POST' and 'phonenum' in request.form and 'password' in request.form:
        PhoneNumber = request.form['phonenum']
        PIN = request.form['password']
        cursor = get_db()
        cursor.execute('INSERT INTO user_login VALUES (?, ?)', (PhoneNumber, PIN))
        cursor.commit()
        msg = 'You have successfully registered !'
        
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('user_signup.html', msg = msg)

    