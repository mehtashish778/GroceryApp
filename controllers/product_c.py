from main import db
from models.product_db import product


def createProduct(data={}):
    try:
        new_product = product(
            name=data['name'],
            category=data['category'],
            stock=data['stock'],
            description=data['description'],
            image=data['image'],
            price=data['price'],
        )
        db.session.add(new_product)
        db.session.commit()
        return True

    except:
        db.session.rollback()
        return False



def getAllProducts():
    
    return db.session.query(product).all()


def deleteProduct(id=''):
    
    
    del_product = db.session.query(product).filter_by(id=id).first()

    if del_product:
        # Delete the product from the database
        db.session.delete(del_product)
        db.session.commit()
        
    return True

def editProduct(pid, data={}):
    try:
        product = getProduct(id=pid)
        
        for key, value in data.items():
            setattr(product, key, value)
        
        db.session.commit()
        return True
    
    except:
        db.session.rollback()
        return False

def getProduct(id=''):
    show = db.session.query(product).filter(product.id == id).first()
    return show

def getProductByName(name=''):
    shows = db.session.query(product).filter((product.name.like('%'+name+'%'))).all()
    return shows


def getProductByID(id=''):
    shows = db.session.query(product).filter((product.id.like('%'+id+'%'))).all()
    return shows

def getProductByCategory(category=''):
    shows = db.session.query(product).filter((product.category.like('%'+category+'%'))).all()
    return shows

def getProductByDes(des=''):
    shows = db.session.query(product).filter((product.description.like('%'+des+'%'))).all()
    return shows


    