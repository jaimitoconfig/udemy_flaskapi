"""
Using Heroku.

NOTES:
This is a copy of project flask_sqlalchemy folder, which has more comments regarding it's section (section 6).
This will have comments regarding this data base section 7.

07/24/2019
Jaime Quintero
"""
from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt import JWT
from datetime import timedelta

from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList
from security import authenticate, identity as identity_function

app = Flask(__name__)
# Telling SQLALCHEMY what data base to use.
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'  # It can also be MySQL.
# SQLAlchemy can check for object modifications, which can take up resources.
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False, This turns it off from Flask.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'letmein'
api = Api(app)

app.config['JWT_AUTH_URL_RULE'] = '/login'
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=1800)
app.config['JWT_AUTH_USERNAME_KEY'] = 'email'


@app.before_first_request  # This will run the function below, before the first request.
def create_tables():
    # This will create this: 'sqlite:///data.db' and it's tables, unless it exists already.
    # This will gather all table information from the models to help create them.
    db.create_all()


jwt = JWT(app, authenticate, identity_function)
@jwt.auth_response_handler
def customized_response_handler(access_token, identity):
    return jsonify({
        'access_token': access_token.decode('utf-8'),
        'user_id': identity.id
    })


@jwt.jwt_error_handler
def customized_error_handler(error):
    return jsonify({
        'message': error.description,
        'code': error.status_code
    }), error.status_code


api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(UserRegister, '/register')


if __name__ == '__main__':
    from db import db  # This is due to circular imports.
    db.init_app(app)
    app.run(port=5000, debug=True, host='0.0.0.0')
