"""
Using Heroku.

NOTES:
This is a copy of project flask_sqlalchemy folder, which has more comments regarding it's section (section 6).
This will have comments regarding this data base section 7.

The runtime.txt file is so that Heroku knows what language to use.

requirements.txt can be generated by pip, I'm using the txt file from the last lecture.
only added uwsgi.

uWSGI is a full fledged http server.
uwsgi.ini is the configuration file for uwsgi.

Procfile will tell Heroku were to find the configuration files (uwsgi.ini)

When you run uwsgi, it will not start at if __name__ == '__main__'. It will start at the beginning of the app.py file.
This is why we need to make a separate file: run.py, or else we can cause circular imports.

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
