import os

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from flask_cors import CORS


from security import authenticate,identity
from resources.user import UserRegister
from resources.store import Store,StoreList
from resources.item import Item,ItemList


app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
#app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///my_database.db"
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL','sqlite:///my_database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'sriju'
api = Api(app)

jwt = JWT(app,authenticate,identity)

api.add_resource(Store,'/store/<string:name>')
api.add_resource(Item,'/item/<string:name>') 
api.add_resource(ItemList,'/items')
api.add_resource(UserRegister,'/register')
api.add_resource(StoreList,'/stores')

if __name__ == '__main__':
    app.run(port=5000, debug=True)