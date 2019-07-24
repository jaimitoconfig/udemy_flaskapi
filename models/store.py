"""
Store Model.

NOTE:
A resource will typically need to extract information for a model. Make the models first.

06/27/2019
Jaime Quintero
"""
from db import db


class StoreModel(db.Model):
    __tablename__ = 'stores'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    # This is considered a back reference, which checks to see what items are assigned to what store.
    # items is a list of ItemModel objects. A many to one relationship.
    # lazy='dynamic' tells SQLAlchemy to not create objects, yet. .all() will take care of that.
    # That makes items a query builder.
    items = db.relationship('ItemModel', lazy='dynamic')  # In ItemModel the foreignKey() checks for what is related.

    def __init__(self, name):
        self.name = name

    def store(self):
        """Simply returns a dictionary representation of the store, with it's items. """
        # .all() will fetch all the items since items is a query builder.
        # It's possible that this is slower since it's looking into the data base.
        # Instead of saving all objects and then iterating.
        # That's how SQLAlchemy works—we use self to refer to the content related to this particular object
        return {'name': self.name, 'items': [item.item() for item in self.items.all()]}  # Has to be self.items.

    def save_to_db(self):
        """Saving an store into the DB. """
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        """Deleting a store in the DB. """
        # Remember that the store can not have items linked if deleting.
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_name(cls, name):
        """This will find the store specified by the name param in DB using SQLAlchemy. """
        return cls.query.filter_by(name=name).first()

