from flask import request,render_template,redirect, url_for

from main import app
from main import get_db
from main import session
from models import *


@app.route('/')
def h():
    
    return redirect(url_for('home'))

    


@app.route('/login', methods =['GET','POST'])
def login():
    msg = ''
    
    a=4
    if request.method == 'POST' and 'phonenum' and 'password' in request.form:
        PhoneNumber = request.form['phonenum']
        PIN = request.form['password']
        cursor = get_db()
        result = cursor.execute('SELECT * FROM user_login WHERE PhoneNumber = ? AND PIN = ?', (PhoneNumber, PIN))
        user = result.fetchone()
        
        if user:
            session['username'] = str(user[0])
            return redirect(url_for('home'))
        else:
            msg = 'Invalid Details'
            
    return render_template('signin.html',msg=msg)
        
        
