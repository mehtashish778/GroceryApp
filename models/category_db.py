from main import db

class category(db.Model):
    __tablename__='category'
    
    name=db.Column(db.Text,nullable=False,primary_key=True,unique=True)