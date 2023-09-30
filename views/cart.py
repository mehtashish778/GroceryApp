from flask import flash,request,render_template,redirect, url_for

from main import app
from main import get_db
from main import session
from models import *
from controllers import cart_c



@app.route('/home/cart',methods =['GET','POST'])
def cart():
    uname =session['username']
    if uname:
        plist = cart_c.getCart(uname)
        total_amt = total(plist)
    else:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
            if 'place_order' in request.form:
                
            
                flag  = cart_c.placeOrder(uname)
                
                if flag:
                    redirect (url_for('order_conf'))
                else:
                    flash("Something went wrong!! Please delete unavaiable products from cart")
 
                
    return render_template('user_cart.html',plist=plist,total_amt = total_amt,link=url_for('logout'), id="Logout")
    
def total(p_list):
    sum = 0
    for i in p_list:
        sum += i[3]*i[5]
    return sum




@app.route('/home/<pid>',methods =['GET','POST'])
def addtocart(pid):
    
    uname =session['username'] 
    if uname:
        cart_c.AddToCart(pid=pid,customer_id=uname)
               
    else:
        return redirect(url_for('login'))
    
    return redirect(url_for('home'))



@app.route('/order-confirmation')
def order_conf():
    return render_template('order_conf.html')




@app.route('/cart/<cart_id>',methods = ['POST'])
def update_cart(cart_id):
    
    
    if request.method == 'POST':
        if 'decrease' in request.form:
            cart_c.updateCart(cart_id=cart_id,ttd="minus")
        elif 'increase' in request.form:
            cart_c.updateCart(cart_id=cart_id,ttd="plus")
        else:
            redirect(url_for('home'))
    
    return redirect(url_for('cart'))

            


            
            






        