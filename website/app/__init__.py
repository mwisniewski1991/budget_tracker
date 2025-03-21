from flask import Flask
from sqlalchemy import text
# from sqlalchemy.schema import DDL
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from os import environ
import logging

db = SQLAlchemy()

# Move models import to global level
from .models import (Owners, Accounts, Type, Category, 
                    Subategory, INCEXP_header, INCEXP_position)

def create_app():

    app = Flask(__name__)
    app.config.from_prefixed_env()

    db.init_app(app)
    migrate = Migrate(app, db)

    from .custom_sql import insert_types

    with app.app_context():       
        db.session.execute(text("CREATE SEQUENCE IF NOT EXISTS accounts_id_seq;"))
        db.session.execute(text("CREATE SEQUENCE IF NOT EXISTS category_id_seq;"))
        db.session.execute(text("CREATE SEQUENCE IF NOT EXISTS subcategory_id_seq;"))
        db.session.commit()

        db.create_all()
        
        db.session.execute(text(insert_types))
        db.session.commit()

    from .views import views
    from .blueprints.accounts_results.accounts_results import accounts_results
    from .blueprints.owners.owners import owners
    from .blueprints.incexp.incexp import incexp
    from .blueprints.types.types import types

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(accounts_results, url_prefix='/accounts-results')
    app.register_blueprint(owners, url_prefix='/owners')
    app.register_blueprint(incexp, url_prefix='/incexp')
    app.register_blueprint(types, url_prefix='/type')


    return app

def initital_database_objects():
    pass