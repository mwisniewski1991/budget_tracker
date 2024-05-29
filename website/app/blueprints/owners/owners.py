from flask import Blueprint, render_template, request, send_from_directory, redirect, jsonify
from sqlalchemy import text, and_, select, func, case, alias
from ... import db
from ...models import Owners, OwnersSchema, Accounts
import logging

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)

owners = Blueprint (
                    'owners', 
                    __name__,
                    template_folder="templates",
                    static_folder="static")


@owners.route("/", methods=['GET'])
def accounts_results_home():
    owners = Owners.query.order_by(Owners.id).all()
    return render_template("owners/home.html.jinja", owners=owners)

@owners.route('/', methods=['POST'])
def add_owners():
    new_owner_name = request.form.get('owner_name_pl', None)
    new_owner = Owners(name_pl=new_owner_name)
    db.session.add(new_owner)
    db.session.commit()

    return redirect('/owners')

@owners.route('/<owner_id>', methods=['PUT'])
def edit_owners(owner_id):
    new_owner_name = request.form.get('owner_name_pl', None)
    owner_existing = Owners.query.filter_by(id = owner_id).one()
    owner_existing.name_pl = new_owner_name

    db.session.commit()
    return render_template("owners/owners_read.html.jinja", owner=owner_existing)

@owners.route('/<owner_id>/edit', methods=['GET'])
def edit_owners_html(owner_id):
    owner = Owners.query.filter_by(id = owner_id).one()
    return render_template("owners/owners_edit.html.jinja", owner=owner)

@owners.route('/<owner_id>/confirmed', methods=['GET'])
def confirmed_owners_html(owner_id):
    owner = Owners.query.filter_by(id = owner_id).one()
    return render_template("owners/owners_read.html.jinja", owner=owner)


# ACCOUNTS
@owners.route('/<owner_id>/accounts', methods=['POST'])
def add_accounts(owner_id):
    new_account_name = request.form.get('account_name_pl', None)
    new_account = Accounts(name_pl = new_account_name, owner_id=owner_id)
    db.session.add(new_account)
    db.session.commit()
    return redirect('/owners')

@owners.route('/<owner_id>/accounts/<account_id>', methods=['PUT'])
def edit_account(owner_id, account_id):
    new_account_name = request.form.get('account_name_pl', None)
    account = Accounts.query.filter_by(id=account_id, owner_id=owner_id).one()
    account.name_pl = new_account_name
    
    db.session.commit()
    return render_template('owners/account_read.html.jinja', account=account)

@owners.route('/<owner_id>/accounts/<account_id>/edit', methods=['GET'])
def edit_accounts_html(owner_id, account_id):
    account = Accounts.query.filter_by(id=account_id, owner_id=owner_id).one()
    return render_template('owners/account_edit.html.jinja', account=account)

@owners.route('/<owner_id>/accounts/<account_id>/read', methods=['GET'])
def read_account_html(owner_id, account_id):
    account = Accounts.query.filter_by(id=account_id, owner_id=owner_id).one()
    return render_template('owners/account_read.html.jinja', account=account)