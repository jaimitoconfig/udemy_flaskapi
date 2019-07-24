"""
User Resource.
This is a resource since it inherits from the Flask Resource.
Resources would be things that APIs communicate with.*
A resource is an external representation of an entity.*

06/26/2019
Jaime Quintero
"""
import sqlite3
from flask_restful import Resource, reqparse

from models.user import UserModel


class UserRegister(Resource):
    """Making a user resource for our API. """
    parser = reqparse.RequestParser()  # Using request parsing to receive proper registering.
    parser.add_argument('username', type=str, required=True, help='This field cannot be left blank!')
    parser.add_argument('password', type=str, required=True, help='This field cannot be left blank!')

    def post(self):
        """Register a user. """
        data = UserRegister.parser.parse_args()
        if UserModel.find_by_username(data['username']):  # Error handling for users that already exists.
            return {'message': 'User already exists. Try /auth.'}, 400
        user = UserModel(**data)  # "**data" is data['username'] and data['password'].
        user.save_to_db()
        return {'message': 'User created successfully'}, 201
