from flask import request,render_template,redirect, url_for
from main import app
from main import product
from main import session
from controllers import product_c
from main import product


# Define the 'home' route with 'GET' and 'POST' methods
@app.route('/home/', methods=['GET', 'POST'])
def home():

    response = product.ProductAPI().get()
    product_list = response[0]
    
    # Check if the 'username' key exists in the session dictionary
    username = session.get('username')

    if username:
        link = url_for('logout')
        id = 'Logout'
    else:
        link = url_for('login')
        id = 'SignIn/SignUp'
            
    return render_template('home.html', plist=product_list, link=link, id=id)
    
    
# Define the 'logout' route with 'GET' and 'POST' methods
@app.route('/home/logout',methods =['GET','POST'])
def logout():
    session['username']=''
    
    # Render the 'logout.html' template
    return render_template('logout.html')



# Define the 'search' route with 'GET' and 'POST' methods
@app.route('/search', methods=['GET', 'POST'])
def search():
    
    # Check if the user is logged in or not, and set the appropriate link and id
    username = session.get('username')
    if username:
        link = url_for('logout')
        id = 'Logout'
             
    else:
        link = url_for('login')
        id = 'SignIn/SignUp'
   
    # Handle the form submission when the request method is 'POST'
    if request.method == 'POST':
        
        
        # Get the search criteria and query from the form data
        search_by = request.form['search_by']  
        search_query = request.form['search_query']


        # Query product based on search criteri and query
        if search_by == 'By_Name':
            query_product = product_c.getProductByName(name=search_query)
        elif search_by == 'By_ProductID':
            query_product = product_c.getProductByID(id=search_query)
        elif search_by == 'By_Category':
            query_product = product_c.getProductByCategory(category=search_query)
        elif search_by == 'By_Description':
            query_product= product_c.getProductByDes(des=search_query)
        

            
            
        

        #Render home page with queried products
        return render_template('home.html', plist=query_product, link=link, id=id)    
    else:
        return redirect(url_for(home))    
