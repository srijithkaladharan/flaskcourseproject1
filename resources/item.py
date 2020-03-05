from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from flask_cors import cross_origin
from models.item import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type = float,
        required = True,
        help = "This field can not be blank"
    )
    parser.add_argument('store_id',
        type = int,
        required = True,
        help = "Every item needs a storeid"
    )

    @cross_origin()
    @jwt_required()
    def get(self,name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message':'Item not found'},404

    @cross_origin()
    def post(self,name):
        item = ItemModel.find_by_name(name)
        if item:
            return {'message':'An item with name {} already exists'.format(name)},400
        data = Item.parser.parse_args()

        item = ItemModel(name,**data)
        try:
            item.save_to_db()
        except:
            return {'message':'an error occurred inserting the item'}, 500 #internal server error
        return item.json(),201

    @cross_origin()
    def delete(self,name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        return {'message':'Item Deleted'}

    @cross_origin()
    def put(self,name):
        item = ItemModel.find_by_name(name)
        data = Item.parser.parse_args()
        
        if item==None:
            item = ItemModel(name,**data)
        else:
            item.price = data['price']
            
        item.save_to_db()
        return item.json()
        

class ItemList(Resource):
    @cross_origin()
    def get(self):
        return {'items': list(map(lambda x:x.json(),ItemModel.query.all()))}

        # can also be done with list comprehension
        # [item.json() for item in ItemModel.query.all()]