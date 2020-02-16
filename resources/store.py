from flask_restful import Resource
from models.store import StoreModel


class Store(Resource):
    def get(self,name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {'message':'Store not found'},404

    def post(self,name):
        store = StoreModel.find_by_name(name)
        if store:
            return {'message':'A store with name {} already exists'.format(name)},400
        
        store=StoreModel(name)

        try:
            store.save_to_db()
        except:
            return {'message':'An error occurred while creating the store'},500
        return store.json(),201

    def delete(self,name):
        store = StoreModel.find_by_name(name)

        if store == None:
            return {'message':'Store does not exist'}
        try:
            store.delete_from_db()
        except:
            return {'message':'Something went wrong'},500
        return {'message':'Store - {} was deleted'.format(name)}
        


class StoreList(Resource):
    def get(self):
        return {'stores':list(map(lambda x : x.json(),StoreModel.query.all()))}