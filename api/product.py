from flask_restful import Resource, reqparse, fields, marshal_with
from utils import ValidationError, NotFoundError
from controllers import product_c


create_product_parser = reqparse.RequestParser()
create_product_parser.add_argument('name')
create_product_parser.add_argument('category')
create_product_parser.add_argument('stock')
create_product_parser.add_argument('description')
create_product_parser.add_argument('image')
create_product_parser.add_argument('price')

product_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'category': fields.String,
    'stock': fields.Integer,
    'description': fields.String,
    'image': fields.String,
    'price': fields.Integer,
}

class ProductAPI(Resource):

    def get(self, product_id=None):
        product = None
        if not (product_id is None):
            product = product_c.getProduct(id=product_id)
            if not product:
                raise NotFoundError() 
        else:
            product = product_c.getAllProducts()
        return product,200
    

    def delete(self, product_id):
        deleted = product_c.deleteProduct(product_id)
        if (deleted):
            return {'message': 'Product deleted'}, 204
        else:
            return {'message': 'Something went wrong'} , 400
    
    @marshal_with(product_fields)
    def put(self, product_id):
        args = create_product_parser.parse_args()
        name = args.get("name", None)
        category = args.get("category", None)
        stock = args.get("stock", None)
        description = args.get("description", None)
        image = args.get("image", None)
        price = args.get("price", None)


        if product_id is None:
            raise ValidationError(code=400, message="No Product ID provided")
        
        if name is None:
            raise ValidationError(code=400, message="No name provided")
        
        if category is None:
            raise ValidationError(code=400, message="No category provided") 

        if stock is None:
            raise ValidationError(code=400, message="No stock provided") 

        if description is None:
            raise ValidationError(code=400, message="No description provided")
        
        if image is None:
            raise ValidationError(code=400, message="No image provided") 

        if price is None:
            raise ValidationError(code=400, message="No price provided")

        
        data = dict()
        data['name'] = name
        data['category'] = category
        data['stock'] = stock
        data['description'] = description
        data['image'] = image
        data['price'] = price

        updated_product = product_c.editProduct(pid=product_id,data=data)

        if updated_product:
            return {'message': 'Product updated'}, 200
        else:
            return {'message': 'Something went wrong'} , 400
    
    
    @marshal_with(product_fields)
    def post(self):
        args = create_product_parser.parse_args()
        name = args.get("name", None)
        category = args.get("category", None)
        stock = args.get("stock", None)
        description = args.get("description", None)
        image = args.get("image", None)
        price = args.get("price", None)

        
        if name is None:
            raise ValidationError(code=400, message="No name provided")
        
        if category is None:
            raise ValidationError(code=400, message="No category provided") 

        if stock is None:
            raise ValidationError(code=400, message="No stock provided") 

        if description is None:
            raise ValidationError(code=400, message="No description provided")
        
        if image is None:
            raise ValidationError(code=400, message="No image provided") 

        if price is None:
            raise ValidationError(code=400, message="No price provided")

        
        data = dict()
        data['name'] = name
        data['category'] = category
        data['stock'] = stock
        data['description'] = description
        data['image'] = image
        data['price'] = price

        added_product = product_c.createProduct(data=data)

        if added_product:
            return {'message': 'Product Added'}, 200
        else:
            return {'message': 'Something went wrong'} , 400