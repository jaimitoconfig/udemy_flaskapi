"""
Setting up Flask-SQLAlchemy.
Basically this will link to our Flask app and link objects to rows in the data base.

NOTE:

06/26/2019
Jaime Quintero
"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()  # Initialize SQLAlchemy.
