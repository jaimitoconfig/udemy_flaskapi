"""
Store Resource.

NOTE:

06/27/2019
Jaime Quintero
"""
from flask_restful import Resource

from models.store import StoreModel


class Store(Resource):
    def get(self, name):
        """
        This will return an store specified by the name param.
        If not found will return None and 404 error code.
        """
        store = StoreModel.find_by_name(name)  # This now returns an object, opposed to a dict (section 5).
        if store:
            return store.store()
        return {'message': 'No store found. Try POST.'}, 404

    def post(self, name):
        """
        Creates a store model and saves it to the data base.
        Returns store dict and 201 code.
        """
        if StoreModel.find_by_name(name):  # Error control.
            return {'message': 'A store with this name already exists.'}, 400
        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {'message': 'An error has occurred saving to the data base.'}, 500
        return store.store(), 201

    def delete(self, name):
        """Removes the store from DB using the store model. """
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()
        return {'message': 'Store deleted.'}


class StoreList(Resource):
    def get(self):
        """Returns a dict with all store data. """
        return {'stores': [store.store() for store in StoreModel.query.all()]}
