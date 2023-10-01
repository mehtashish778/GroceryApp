from main import db
from models.category_db import category
from models.product_db import product
from controllers import product_c




def createCategory(new_cat_name):
    try:
        new_category = category(name=new_cat_name)
        db.session.add(new_category)
 
    except:
        db.session.rollback()
        raise Exception('DB error.')
    
    else:
        db.session.commit()
        return True


def getAllCategory():
    
    return db.session.query(category).all()


def deleteCategory(name=''):
    
    del_category = db.session.query(category).filter_by(name=name).first()

    if del_category:
        db.session.delete(del_category)
        
        prod_list = product_c.getProductByCategory(category=name)
        for prod in prod_list:
            product_c.deleteProduct(id=prod.id)
        
        db.session.commit()
    return True



def getCategory(name=''):
    show = db.session.query(category).filter(category.name == name).first()
    return show


def updateCategory(old_name,new_name):
        
    try:

        category_to_updated = getCategory(name=old_name)

        # Update the name attribute of the category object.
        category_to_updated.name = new_name
        
        product_to_update = product_c.getProductByCategory(category=old_name)
        
        for prod in product_to_update:
            prod.category = new_name

    

    except:
        db.session.rollback()
        raise Exception('DB error.')
    else:
        db.session.commit()
        return True
    
    
    
    