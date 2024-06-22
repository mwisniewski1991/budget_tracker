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

    # app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://budget_user:KY]bU)km+}VMV#4,fm@192.168.0.142:5432/budget_tracker'
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://mw:mw@192.168.0.101:5432/budget_tracker_test'
    # app.config['SECRET_KEY'] = '123_456_789'
    # app.config['DEFAULT_RESULTS_LIMIT'] = 50

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
    from .blueprints.incomes_categories.incomes_categories import incomes_categories

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(accounts_results, url_prefix='/accounts-results')
    app.register_blueprint(owners, url_prefix='/owners')
    app.register_blueprint(incexp, url_prefix='/incexp')
    app.register_blueprint(incomes_categories, url_prefix='/incomes-categories')


    return app
