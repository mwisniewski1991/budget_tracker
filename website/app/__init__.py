from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from os import environ
from dotenv import load_dotenv

db = SQLAlchemy()

def create_app():
    # basedir = path.abspath(path.dirname(__file__))
    # load_dotenv(path.join(basedir, ".env"))

    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('SQLALCHEMY_DATABASE_URI')

    db.init_app(app)
    migrate = Migrate(app, db)

    from .models import Owners, Accounts, Type, Category, Subategory, INCEXP_header, INCEXP_position
    with app.app_context():
        db.create_all()

    from .views import views
    app.register_blueprint(views, url_prefix='/')


    return app
