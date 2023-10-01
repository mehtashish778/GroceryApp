from sqlalchemy.ext.declarative import declarative_base
from flask_sqlalchemy import SQLAlchemy

engine = None
Base = declarative_base()

from main import db
from .product_db import *
from .category_db import *
from .cart_db import *




class admin_login(db.Model):
    __tablename__ = 'admin_login'
    PhoneNumber = db.Column(db.Integer,unique=True,nullable=False,primary_key=True)
    PIN=db.Column(db.Integer,nullable=False)
    
class user_login(db.Model):
    __tablename__='user_login'
    PhoneNumber = db.Column(db.Integer,unique=True,nullable=False,primary_key=True)
    PIN=db.Column(db.Integer,nullable=False)

