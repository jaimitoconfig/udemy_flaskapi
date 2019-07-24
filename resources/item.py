"""
Item Resources.

NOTE:

06/26/2019
Last edited: 06/27/2019
Jaime Quintero
"""
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True, help='This field cannot be left blank!')
    parser.add_argument('store_id', type=int, required=True, help='All items need a store id!')

    @jwt_required()
    def get(self, name):
        """
        This will return an item specified by the name param.
        If not found will return None and 404 error code.
        """
        try:
            item = ItemModel.find_by_name(name)  # This now returns an object, opposed to a dict (section 5).
        except:
            return {'message': 'An error has occurred selecting.'}, 500
        if item:
            return item.item()  # item() method returns a dictionary representation of the ItemModel object.
        return {'message': 'No item found. Try POST.'}, 404

    def post(self, name):
        """
        Retrieves JSON payload, place values into dict, inserts data into DB.
        Returns item dict and 201 code.
        """
        if ItemModel.find_by_name(name):  # Error control.
            return {'message': 'An item with this name already exists. Try PUT.'}, 400
        data = Item.parser.parse_args()
        item = ItemModel(name, **data)
        try:
            item.save_to_db()  # Inserts itself into the data base.
        except:
            return {'message': 'An error has occurred saving.'}, 500
        return item.item(), 201

    def delete(self, name):
        """Removes the item from DB using the item model. """
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        else:
            return {'message': 'An item with this name does NOT exists. Try POST.'}, 400
        return {'message': 'Item deleted.'}

    def put(self, name):
        """Create item, or update existing item. """
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)  # This now returns an object.
        if not item:
            item = ItemModel(name, **data)  # Create item if none exists.
        else:
            item.price = data['price']  # Basically updating the price only, if it does exist.
        item.save_to_db()  # Save any changes or a new item if there was none.
        return item.item()


class ItemList(Resource):
    def get(self):
        """Returns items list. """
        # THIS IS IMPORTANT 06/27/2019 ###################################################################
        # Make a list comprehension that will iterate through all the items objects in the data base table.
        # Doing this with lambda - list(map(lambda x: x.item(), ItemModel.query.all()))
        # Using list comprehensions is more "Pythonic", lambda would be used to help others understand.
        return {'items': [item.item() for item in ItemModel.query.all()]}  # .all(), returns all items in data base.
