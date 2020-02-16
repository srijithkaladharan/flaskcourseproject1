from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from db import db

from security import authenticate,identity
from resources.user import UserRegister
from resources.store import Store,StoreList
from resources.item import Item,ItemList
#from resources.store import Store,StoreList


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///my_database.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# this turns off Flask's SQL Achemy tracker and not the SQL Alchemy's own tracker
app.secret_key = 'sriju'
api = Api(app)

@app.before_first_request
def create_table():
    db.create_all()

jwt = JWT(app,authenticate,identity)

db.init_app(app)

api.add_resource(Store,'/store/<string:name>')
api.add_resource(Item,'/item/<string:name>') 
api.add_resource(ItemList,'/items')
api.add_resource(UserRegister,'/register')
api.add_resource(StoreList,'/stores')

if __name__ == '__main__':
    app.run(port=5000, debug=True)