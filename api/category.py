from flask_restful import Resource, reqparse, fields, marshal_with
from utils import ValidationError, NotFoundError
from controllers import product_c,category_c

create_category_parser = reqparse.RequestParser()
create_category_parser.add_argument('name')


category_fields = {
    'name': fields.String
}

class CategoryAPI(Resource):
    
    
    def get(self, category_name=None):
        category = None
        if not (category_name is None): 
            category = category_c.getCategory(name=category_name)
            if not category:
                raise NotFoundError() 
        else:
            category = category_c.getAllCategory()
        return category,200
    
    
    def delete(self, category_name):
        deleted = category_c.deleteCategory(name=category_name)
        if (deleted):
            return {'message': 'Product deleted'}, 200
        else:
            return {'message': 'Something went wrong'} , 400
        
    @marshal_with(category_fields)
    def post(self):
        args = create_category_parser.parse_args()
        name = args.get("name", None)
        
        flag = False
        
        category_exist = category_c.getCategory(name=name)
        
        if name != category_exist:
            category_c.createCategory(new_cat_name=name)
            return True, 200
        else:
            return False, 400
    
    @marshal_with(category_fields)
    def put(self,category_name):
        args = create_category_parser.parse_args()
        name = args.get("name", None)
        
        flag = False
        flag =category_c.updateCategory(category_name,name)
        if flag:
            return True, 200
        else:
            return False, 400
        
        
        
        
        
        
        
    
    
    
        
        