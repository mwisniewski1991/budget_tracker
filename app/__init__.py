from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from os import path

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://mw:test@localhost:5432/budget_test"
    db.init_app(app)
    migrate = Migrate(app, db)

    from .views import views
    app.register_blueprint(views, url_prefix='/')


    return app