from flask import Blueprint, render_template, request, send_from_directory, redirect, jsonify
from sqlalchemy import text, and_, select, func, case, alias
from ... import db
from ...models import Owners, INCEXP_header, INCEXP_position, Category, Subategory
from .forms import Incexp_header_form
from .utils import category_subcategory_decrypt, category_subcategory_encrypt
import logging

DEFAULT_OWNER_ACCOUNT_IDS = '1_05'
DEFAULT_EMPTY_CHOICE = '00_0000'

incexp = Blueprint (
                    'incexp', 
                    __name__,
                    template_folder="templates",
                    static_folder="static")

@incexp.route('/', methods=['GET'])
def get_incexp():
    owner_account_ids = request.args.get('owner-account-ids', DEFAULT_OWNER_ACCOUNT_IDS)
    owner_id, account_id = owner_account_ids.split('_')

    results_limit = request.args.get('limit', 50)
    type_id = request.args.get('type-id', None)
    source = request.args.get('source',  None)
    created_date_from = request.args.get('created_date_from',  None)
    created_date_to = request.args.get('created_date_to',  None)
    comment = request.args.get('comment', None)
    connection = request.args.get('connection', None)

    incexp_list = (INCEXP_header
                .query
                .filter(and_(INCEXP_header.owner_id==owner_id, INCEXP_header.account_id==account_id))
                )
    
    if type_id:
        incexp_list = incexp_list.filter(INCEXP_header.type_id == type_id)


    if created_date_from:
        incexp_list = incexp_list.filter(INCEXP_header.date >= created_date_from)

    if created_date_to:
        incexp_list = incexp_list.filter(INCEXP_header.date <= created_date_to)
    
    if source:
        incexp_list = incexp_list.filter(INCEXP_header.source.ilike(f'%{source}%'))

    if created_date_from:
        incexp_list = incexp_list.filter(INCEXP_header.date >= created_date_from)

    if comment:
        incexp_list = incexp_list.filter(INCEXP_header.incexp_positions.any(INCEXP_position.comment.ilike(f"%{comment}%")))

    if connection:
        incexp_list = incexp_list.filter(INCEXP_header.incexp_positions.any(INCEXP_position.connection.ilike(f"%{connection}%")))


    incexp_list = (incexp_list
                    .order_by(INCEXP_header.date.desc(), INCEXP_header.id)
                    .limit(results_limit)
                   ).all()

    owners = Owners.query.order_by(Owners.id).all()

    choices_list = []
    for owner in owners:
        for account in owner.accounts:
            choices_list.append(f'{owner.id}_{account.id}')

    incexp_header_form = Incexp_header_form()
    incexp_header_form.owner_accounts_ids.choices = choices_list

    return render_template("incexp/home.html.jinja", 
                            incexp_list=incexp_list, 
                            incexp_header_form=incexp_header_form, 
                            owners=owners,
                            owner_account_ids=owner_account_ids)

@incexp.route('/', methods=['POST'])
def add_incexp():

    owner_account_ids = request.args.get('owner-account-ids', DEFAULT_OWNER_ACCOUNT_IDS)

    incexp_header_form = Incexp_header_form()
    owner_id, account_id =  category_subcategory_decrypt(incexp_header_form.owner_accounts_ids.data)

    new_incexp_header = INCEXP_header(
        date  = incexp_header_form.date.data,
        source = incexp_header_form.source.data,
        owner_id = owner_id,
        account_id = account_id,
        type_id = incexp_header_form.type.data,
    )
    db.session.add(new_incexp_header)
    db.session.commit()

    for index, position in enumerate(incexp_header_form.positions):
        if position.category.data != DEFAULT_EMPTY_CHOICE: 

            category_id, subcategory_id = category_subcategory_decrypt(position.category.data)    

            new_incexp_position = INCEXP_position(
                header_id = new_incexp_header.id,
                position_id = index + 1,
                category_id = category_id,
                subcategory_id = subcategory_id,
                amount = position.amount.data,
                comment = position.comment.data,
                connection = position.connection.data,
            )
            db.session.add(new_incexp_position)
    db.session.commit()

    return redirect("/incexp")


@incexp.route('/owners-accounts', methods=['GET'])
def get_owners_accounts():
    owners = Owners.query.order_by(Owners.id).all()
    return render_template("incexp/owners_accounts_dropdown.html.jinja", owners=owners)

@incexp.route("/categories",  methods=['GET'])
def get_categories():
    type_id = request.args.get('type-id', None)
    if type_id:
        categories = Category.query.filter_by(type_id= type_id).all()
        return render_template("incexp/categories_select.html.jinja", categories=categories)
    return 'Bad request! No parameters', 400

@incexp.route("/subcategories",  methods=['GET'])
def get_subcategories():
    category_id = request.args.get('category-id', None)
    if category_id:
        subcategories = Subategory.query.filter_by(category_id=category_id).all()
        return render_template("incexp/categories_select.html.jinja", categories=subcategories)
    return 'Bad request! No parameters', 400

@incexp.route("/positions",  methods=['GET'])
def get_position_html():
    type_id = request.args.get('type-id', None)
    categories_subcategories = (db.session
                                    .query(Category.id,
                                           Category.name_pl,
                                           Subategory.id,
                                           Subategory.name_pl,
                                           )
                                    .join(Subategory, Category.id == Subategory.category_id)
                                    .filter(Category.type_id == type_id)
                                ).all()
    choices_list = [(category_subcategory_encrypt(cat_sub[0], cat_sub[2]),  f'{cat_sub[1].strip()} : {cat_sub[3].strip()}') for cat_sub in categories_subcategories]
    empty_choice = [(category_subcategory_encrypt('00','0000'), '')]
    choices_list = [*empty_choice, *choices_list]

    incexp_header_form = Incexp_header_form()
    for position in incexp_header_form.positions:
        position.category.choices = choices_list


    return render_template("incexp/incexp_position.html.jinja", incexp_header_form=incexp_header_form)