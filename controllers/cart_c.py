from main import db
from models.cart_db import cart
from models.product_db import product
from sqlalchemy import and_


def getCart(customer_id):
    
    return db.session.query(cart.cartid,cart.customerid,cart.productid,cart.quantity,product.name,product.price,product.stock).join(product, cart.productid == product.id).filter(cart.customerid == customer_id).all()


def getCartItemByID(cart_id):
    return db.session.query(cart).filter_by(cartid=cart_id).first()


def AddToCart(pid,customer_id):
    cart_item = cartByPID_CID(pid,customer_id)
    
    if cart_item:
        updateCart(cart_id=cart_item[0],ttd='plus')
        return True
    else:
        db.session.add(cart(customerid=customer_id, productid=pid, quantity=1))
        db.session.commit()
        return True
    
        
        
        

def placeOrder(customer_id):
    cart_items = getCart(customer_id)
    flag = True
    
    try:
        with db.session.begin_nested():  # Start a nested transaction
            for i in cart_items:
                itemQuantity = i[3]
                itemStock = i[6]
                if itemQuantity > itemStock:
                    flag = False
                    break
                
                # Decrease the stock by the ordered quantity
                db.session.query(product).filter_by(id=i[2]).update({product.stock: product.stock - itemQuantity})
                
                # Remove the item from the cart
                db.session.query(cart).filter_by(cartid=i[0]).delete()
    except:
        db.session.rollback()
        raise Exception('DB error.')   # Rollback the nested transaction
    else:
        db.session.commit()
        return True



def cartByPID_CID(pid,cid):
    return db.session.query(cart.cartid).filter_by(customerid=cid,productid = pid).first()


def updateCart(cart_id,ttd):
    if ttd == "plus":
        db.session.query(cart).filter_by(cartid=cart_id).update({cart.quantity: cart.quantity + 1})
        db.session.commit()
        return True
    elif ttd == "minus":
        db.session.query(cart).filter(and_(cart.cartid == cart_id, cart.quantity > 0)).update({cart.quantity: cart.quantity - 1})
        db.session.commit()

        return True
    else:
        return False
        

            
    


    
