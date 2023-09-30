from flask import request,render_template,flash,redirect, url_for,flash

from main import app
from main import get_db
from main import session
from controllers import category_c,product_c
from models import product_db
from main import product,category
import requests
import json






# Define the 'search' route with 'GET' and 'POST' methods
@app.route('/admin_search', methods=['GET', 'POST'])
def admin_search():
    
    # Check if the user is logged in or not, and set the appropriate link and id
    username = session.get('username')
    if username:
        link = url_for('logout')
        id = 'Logout'
        category_list = category_c.getAllCategory()

             
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
        return render_template('admin_dashboard.html', plist=query_product, category_list=category_list,link=link, id=id)    
    else:
        return redirect(url_for(dashboard))    




#----------------------------------------------------------Admin Login-------------------------------------------------------------



@app.route('/admin-login', methods =['GET','POST'])
def adminlogin():
    msg = ''
    if request.method == 'POST' and 'phonenum' in request.form and 'password' in request.form:
        PhoneNumber = request.form['phonenum']
        PIN = request.form['password']
        cursor = get_db()
        result = cursor.execute('SELECT * FROM admin_login WHERE PhoneNumber = ? AND PIN = ?', (PhoneNumber, PIN))
        user = result.fetchone()
        
        if user:
            session['username'] = 'admin'
            
            return redirect(url_for('dashboard'))
        else:
            msg = 'Invalid Details'
            
    return render_template('admin_signin.html',msg = msg)



#----------------------------------------------------------Dashboard-------------------------------------------------------------
#-------------------------------------------------------------ok-------------------------------------------------------------



@app.route('/dashboard', methods =['GET','POST'])
def dashboard():
    

    # Extract username from session
    username = session.get('username')              
    
    # Check if user is an admin, otherwise redirect to admin login page
    if username != 'admin':
        return redirect(url_for('adminlogin'))
        
        
    link = url_for('logout')
    id = 'Logout'

        
        
        
    product_list=''
    category_list=''
    
    
    if username == 'admin':
        response_product = product.ProductAPI().get()   #using Product API
        product_list = response_product[0]
        response_category = category.CategoryAPI().get()
        category_list = response_category[0]
    else:
        redirect(url_for('adminlogin'))
    
    
    return render_template('admin_dashboard.html',product_list = product_list,category_list=category_list,link=link, id=id)



#----------------------------------------------------------Delete Product-------------------------------------------------------------
#---------------------------------------------------------------ok-------------------------------------------------------------



@app.route('/dashboard/del/product/<pid>', methods=['DELETE','GET','PUT'])
def delete_product(pid):
    
    # Extract username from session
    username = session.get('username')              
    
    # Check if user is an admin, otherwise redirect to admin login page
    if username != 'admin':
        return redirect(url_for('adminlogin'))
    
    s=False
    
    if session:
        response = product.ProductAPI().delete(product_id=pid)
    else:
        redirect(url_for('adminlogin'))
            
    return redirect(url_for('dashboard'))


#----------------------------------------------------------Edit Product-------------------------------------------------------------
#---------------------------------------------------------------ok-------------------------------------------------------------


@app.route('/dashboard/edit/product/<pid>', methods =['GET','POST','PUT'])
def edit_product(pid):
    
    
    # Extract username from session
    username = session.get('username')              
    
    # Check if user is an admin, otherwise redirect to admin login page
    if username != 'admin':
        return redirect(url_for('adminlogin'))
    
    
    
    current_product = product_c.getProduct(id = pid)
    category_list = category_c.getAllCategory()
    
    
    data = {}    
    flag = False
    if request.method == 'POST':
        data['name']=request.form['pname']
        data['image']=request.form['pimagelink']
        data['price']=request.form['pprice']
        data['stock']=request.form['pstock']
        data['category']=request.form['pcategory']
        data['description']=request.form['pdescription']
        
        
        
        response = product_c.editProduct(pid=pid,data=data)
        
        if response == 200:
            flash("Poduct edited successfully")
        else:
            flash("Something went Wrong")
        
    
    return render_template('admin_edit_product.html',curProduct = current_product,category_list=category_list)


#----------------------------------------------------------Add NeW Product-------------------------------------------------------------
#---------------------------------------------------------------Ok-------------------------------------------------------------



@app.route('/dashboard/addProduct', methods =['GET','POST','PUT'])
def addProduct():
    
    # Extract username from session
    username = session.get('username')              
    
    # Check if user is an admin, otherwise redirect to admin login page
    if username != 'admin':
        return redirect(url_for('adminlogin'))
    
    category_list = category_c.getAllCategory()
    
    
    data = {}    
    flag = False
    if request.method == 'POST':
        data['name']=request.form['pname']
        data['image']=request.form['pimagelink']
        data['price']=request.form['pprice']
        data['stock']=request.form['pstock']
        data['category']=request.form['pcategory']
        data['description']=request.form['pdescription']
        
        
        
        response = product_c.createProduct(data=data)
    
        if response == True:
            flash("Poduct edited successfully")
        else:
            flash("Something went Wrong")
        

        ##Using Api
        # base_url = request.host_url

        # url = base_url+"product"
        
        # jdata = json.dumps(data)
        # headers = {
        #     "Content-Type": "application/json"
        #     }
        # requests.post(url, data=jdata, headers=headers)

    
    return render_template('admin_add_product.html',category_list=category_list)








#----------------------------------------------------------category block-------------------------------------------------------------
#----------------------------------------------------------category block-------------------------------------------------------------
#----------------------------------------------------------category block-------------------------------------------------------------
#----------------------------------------------------------category block-------------------------------------------------------------
#----------------------------------------------------------category block-------------------------------------------------------------
#----------------------------------------------------------category block-------------------------------------------------------------
#----------------------------------------------------------category block-------------------------------------------------------------
#----------------------------------------------------------category block-------------------------------------------------------------
#----------------------------------------------------------category block-------------------------------------------------------------
#----------------------------------------------------------category block-------------------------------------------------------------
#----------------------------------------------------------category block-------------------------------------------------------------
#----------------------------------------------------------category block-------------------------------------------------------------
#----------------------------------------------------------category block-------------------------------------------------------------









#----------------------------------------------------------Add NeW Category-------------------------------------------------------------
#-----------------------------------------------------------------Ok-----------------------------------------------------------------------------------



#Using API to create new category
@app.route('/dashboard/newCategory', methods=['GET', 'POST', 'PUT'])
def addCategory():
    # Extract username from the session
    username = session.get('username')
    
    # Check if the user is an admin, otherwise redirect to the admin login page
    if username != 'admin':
        return redirect(url_for('adminlogin'))
    
    data = {}
    if request.method == 'POST':
        # Extract the category name from the form data
        data['name'] = request.form['pname']
        
        # Construct the base URL
        base_url = request.host_url
        
        # Create the complete URL for the category endpoint
        url = base_url + "category"
        
        # Convert data to JSON format
        jdata = json.dumps(data)
        
        # Set headers for the POST request
        headers = {
            "Content-Type": "application/json"
        }
        
        # Send a POST request to the category endpoint
        response = requests.post(url, data=jdata, headers=headers)
        
        # Check the response status and display appropriate messages
        if response.status_code == 200:
            flash("Category Added Successfully")
        else:
            flash("Category Already Added")
    
    # Render the admin_add_category.html template
    return render_template('admin_add_category.html')





#-----------------------------------------------------------Delete Category-------------------------------------------------------------
#-----------------------------------------------------------------Ok-----------------------------------------------------------------------------------


@app.route('/dashboard/del/category/<name>')
def delete_category(name):
    

    # Extract username from session
    username = session.get('username')              
    
    # Check if user is an admin, otherwise redirect to admin login page
    
    
    if username != 'admin':
        return redirect(url_for('adminlogin')) 
    
    category_c.deleteCategory(name)
            
    return redirect(url_for('dashboard'))



#-----------------------------------------------------------Edit Category-------------------------------------------------------------
#-----------------------------------------------------------------Ok-----------------------------------------------------------------------------------



@app.route('/dashboard/edit/category/<old_name>', methods=['GET', 'POST', 'PUT'])
def UpdateCategory(old_name):
    
    # Extract username from session
    username = session.get('username')              
    
    # Check if user is an admin, otherwise redirect to admin login page
    if username != 'admin':
        return redirect(url_for('adminlogin'))
    
    
    
    if request.method == 'POST':
        nname = request.form['pname']               # Extract new category name from form
        
        
        # Call updateCategory function to update the category name
        flag = category_c.updateCategory(old_name, nname)      
        
        if flag:
            flash("Category Name Edited Successfully")
        
    # Render the template for editing the category name
    return render_template('admin_edit_category.html', cat_name=old_name)


