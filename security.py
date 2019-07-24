"""
Authentication functions using a data base.

06/26/2019
Jaime Quintero
"""
from werkzeug.security import safe_str_cmp
from models.user import UserModel


def authenticate(username, password):
    """
    Authenticate the user, if the user exists and the password is correct...
    Return user object.
    """
    user = UserModel.find_by_username(username)
    if user and safe_str_cmp(user.password, password):
        return user


def identity(payload):
    """
    JWT passes the payload argument which will contain the user identity.
    Returns user object.
    """
    user_id = payload['identity']
    return UserModel.find_by_id(user_id)
