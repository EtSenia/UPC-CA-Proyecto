from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from os import path

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = 'llave secreta'
    app.config["SQLALCHEMY_DATABASE_URI"] = f'sqlite:///{DB_NAME}'

    db.init_app(app)
    

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from . import models as models
    create_database(app)

    return app

def create_database(app):    
    with app.app_context():
        if not path.exists('instance/' + DB_NAME):
            db.create_all()
            print('Database Created')
        else:
            print("Database ya existente")