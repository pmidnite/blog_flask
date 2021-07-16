from flask_sqlalchemy import SQLAlchemy
from os import path


db = SQLAlchemy()

def create_database(app):
    DB_NAME='database.db'
    db.init_app(app)
    if not path.exists('blog/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')