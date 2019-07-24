"""
Item Model.
In the item resources there were methods that do not interact with the client.
These methods were moved here as these interactions are internal not external.

NOTE:
Having an id is essential for data bases.

SQLAlchemy can handle the following, connection, cursor, and queries:
"
connection = sqlite3.connect('data.db')
cursor = connection.cursor()
query = "SELECT * FROM items WHERE name=?"
"
It can also automatically convert the "row" into an object if it can.

06/26/2019
Last edited: 06/27/2019
Jaime Quintero
"""
from db import db


class ItemModel(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))  # This will be a decimal like: 14.99.
    # The foreignKey() in this instance will be linked to a stores id.
    # SQL will NOT let you delete a store with items if their is a foreignKey reference to it.
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
    # This is considered a join. It makes a relationship between this values.
    store = db.relationship('StoreModel')

    def __init__(self, name, price, store_id):
        self.name = name
        self.price = price
        self.store_id = store_id  # This is to match the item to it's store.

    def item(self):
        """Simply returns a dictionary representation of the item object."""
        return {'name': self.name, 'price': self.price}

    def save_to_db(self):
        """Saving an item into the DB. """
        # self argument is letting it know what it will be storing.
        # A session is a collection of objects that will be written to the data base.
        # A session can also help with updating the data.
        db.session.add(self)  # SQLAlchemy can easily store objects.
        db.session.commit()  # Store to data base.

    def delete_from_db(self):
        """Deleting an item in the DB. """
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_name(cls, name):
        """
        This will find the item specified by the name param in DB using SQLAlchemy.
        Returns ItemObject object.
        This is what it used to be:
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()
        """
        # query comes from db. This will help build a query to retrieve specified data.
        # .first() fetches the first one in the tables.
        return cls.query.filter_by(name=name).first()  # "SELECT * FROM __tablename__ WHERE name=name LIMIT 1"
