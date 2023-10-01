from main import db

class cart(db.Model):
    __tablename__ = 'cart'
    cartid=db.Column(db.Integer,primary_key=True,autoincrement=True)
    customerid =db.Column(db.Integer,db.ForeignKey("user_login.PhoneNumber"),nullable=True)
    productid=db.Column(db.Integer,db.ForeignKey("product.id"),nullable=True)
    quantity=db.Column(db.Integer,nullable=False)