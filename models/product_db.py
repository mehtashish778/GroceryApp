from main import db


class product(db.Model):
    __tablename__='product'
    id = db.Column(db.Integer,nullable=False,primary_key=True,autoincrement=True,unique=True)
    name=db.Column(db.Text,nullable=False)
    category=db.Column(db.Text,db.ForeignKey("category.name"),nullable=True)
    stock=db.Column(db.Integer,nullable=False)
    description=db.Column(db.Text,nullable=False)
    image=db.Column(db.Text,nullable=False)
    price=db.Column(db.Integer,nullable=False)