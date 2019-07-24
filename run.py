from app import app
from db import db

db.init_app(app)

# This was in the app.py file, but was moved here.
@app.before_first_request  # This will run the function below, before the first request.
def create_tables():
    # This will create this: 'sqlite:///data.db' and it's tables, unless it exists already.
    # This will gather all table information from the models to help create them.
    db.create_all()
