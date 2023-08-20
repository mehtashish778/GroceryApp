import os
from flask import Flask, render_template, session,redirect, url_for
from flask_restful import Api

from flask import request
from flask_sqlalchemy import SQLAlchemy
import sqlite3
from flask import g
current_dir = os.path.abspath(os.path.dirname(__file__))


app = Flask(__name__)

app.secret_key = 'secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///"+os.path.join(current_dir,"db/grocery_app.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
api = Api(app)
app.app_context().push()


from models import *
from api import *


api.add_resource(CategoryAPI, '/category','/category/<string:category_name>')
api.add_resource(ProductAPI, '/product', '/product/<int:product_id>')

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect('db\grocery_app.db')
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()



@app.errorhandler(404)
def page_not_found(e):
    return render_template('_404.html'), 404


@app.before_request
def before_request():
    g.category=category
    g.product = product

        
from views import *
        


if __name__ == '__main__':
    app.run(debug=True)