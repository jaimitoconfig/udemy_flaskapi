"""
User Model.
Since the API does not need to communicate with this, it is not a Resource.
A model is our internal representation of an entity.*
A resource is an external representation of an entity.*
Essentially a "helper".

db is going to help with mapping these objects to the data base.

06/26/2019
Jaime Quintero
"""
from db import db


class UserModel(db.Model):  # This is now an API. NOT RESTFul API.
    """User object for mapping users in the data base. """
    __tablename__ = 'users'  # This will tell SQLAlchemy what data base table to use.
    # Telling SQLAlchemy what columns to use.
    id = db.Column(db.Integer, primary_key=True)  # Setting up the id column in our data base table.
    username = db.Column(db.String(80))  # db.String(80), 80 is limiting it's character to 80.
    password = db.Column(db.String(80))

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def save_to_db(self):
        """Storing directly to the data base. """
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):  # Retrieve user information by username.
        """Username mapping. """
        # "SELECT * FROM __tablename__ WHERE username=username LIMIT 1"
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id):  # Retrieve user information by id.
        """User ID mapping. Mainly used in authentication. """
        # "SELECT * FROM __tablename__ WHERE id=_id LIMIT 1"
        return cls.query.filter_by(id=_id).first()
