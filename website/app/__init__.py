from flask import Flask
from sqlalchemy import text
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from os import environ
import logging

db = SQLAlchemy()

def create_app():

    app = Flask(__name__)
    app.config.from_prefixed_env()

    db.init_app(app)
    migrate = Migrate(app, db)

    from .models import Owners, Accounts, Type, Category, Subategory, INCEXP_header, INCEXP_position
    from .custom_sql import accounts_id_seq_custom, insert_types

    with app.app_context():
        db.create_all()

    from .views import views
    from .blueprints.accounts_results.accounts_results import accounts_results
    from .blueprints.owners.owners import owners
    from .blueprints.incexp.incexp import incexp

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(accounts_results, url_prefix='/accounts-results')
    app.register_blueprint(owners, url_prefix='/owners')
    app.register_blueprint(incexp, url_prefix='/incexp')

    return app
