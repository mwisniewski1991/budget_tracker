from flask import Blueprint, render_template, url_for, request, send_from_directory, redirect, jsonify
from sqlalchemy import text, and_, select, func, case, alias
from ... import db
from ...models import Owners, INCEXP_header, INCEXP_position, Category, Subategory
from .forms import Incexp_header_form
from .utils import master_slave_decrypt, master_slave_encrypt, incexp_query_existings
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
    owner_id, account_id = master_slave_decrypt(owner_account_ids)

    results_limit = request.args.get('limit', 50)
    type_id = request.args.get('type-id', None)
    source = request.args.get('source',  None)
    created_date_from = request.args.get('created_date_from',  None)
    created_date_to = request.args.get('created_date_to',  None)
    comment = request.args.get('comment', None)
    connection = request.args.get('connection', None)

    incexp_list = incexp_query_existings(
        results_limit,
        owner_id,
        account_id,
        type_id,
        created_date_from,
        created_date_to,
        source,
        comment,
        connection,
    )


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

    incexp_header_form = Incexp_header_form()
    owner_id, account_id =  master_slave_decrypt(incexp_header_form.owner_accounts_ids.data)

    if any([position.amount.data for position in incexp_header_form.positions]):
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
                category_id, subcategory_id = master_slave_decrypt(position.category.data)    

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

    results_limit = request.args.get('limit', 50)

    incexp_list = incexp_query_existings(results_limit, owner_id, account_id)

    return render_template('incexp/incexp_list_existing.html.jinja', incexp_list=incexp_list)

@incexp.route('/<header_id>', methods=['DELETE'])
def delete_incexp(header_id):
    INCEXP_position.query.filter_by(header_id=header_id).delete()
    INCEXP_header.query.filter_by(id=header_id).delete()
    db.session.commit()
    return ""

@incexp.route('/<header_id>/edit', methods=['GET'])
def get_incexp_edit(header_id):
    incexp_header_form = Incexp_header_form()
    incexp = (INCEXP_header
            .query
            .filter(INCEXP_header.id==header_id)
            ).first()

    categories_subcategories = (db.session
                                .query(Category.id,
                                        Category.name_pl,
                                        Subategory.id,
                                        Subategory.name_pl,
                                        )
                                .join(Subategory, Category.id == Subategory.category_id)
                                .filter(Category.type_id == incexp.type_id)
                            ).all()
    choices_list = [(master_slave_encrypt(cat_sub[0], cat_sub[2]),  f'{cat_sub[1].strip()} : {cat_sub[3].strip()}') for cat_sub in categories_subcategories]

    incexp_header_form.source.data = incexp.source
    incexp_header_form.date.data = incexp.date
    incexp_header_form.type.data= incexp.type_id


    for position in incexp.incexp_positions:
        incexp_header_form.positions[position.position_id].category.choices = choices_list
        incexp_header_form.positions[position.position_id].category.data = master_slave_encrypt(position.category_id, position.subcategory_id)

        incexp_header_form.positions[position.position_id].amount.data = position.amount_absolute
        incexp_header_form.positions[position.position_id].comment.data = position.comment
        incexp_header_form.positions[position.position_id].connection.data = position.connection


    return render_template("incexp/incexp_edit.html.jinja", incexp=incexp, incexp_header_form=incexp_header_form)

@incexp.route('/<header_id>/edit', methods=['POST'])
def edit_incexp(header_id):
    
    incexp_header_form = Incexp_header_form()
    incexp = (INCEXP_header
        .query
        .filter(INCEXP_header.id==header_id)
        ).first()
    
    incexp.date  = incexp_header_form.date.data,
    incexp.source = incexp_header_form.source.data,
    incexp.type_id = incexp_header_form.type.data,

    for index, position in enumerate(incexp_header_form.positions):
        if not position.category.data is None: 
            category_id, subcategory_id = master_slave_decrypt(position.category.data)    

            incexp.incexp_positions[index].category_id = category_id,
            incexp.incexp_positions[index].subcategory_id = subcategory_id,
            incexp.incexp_positions[index].amount = position.amount.data,
            incexp.incexp_positions[index].comment = position.comment.data,
            incexp.incexp_positions[index].connection = position.connection.data,

    db.session.commit()

    return 'Zmieniono'

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
    return ''

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
    choices_list = [(master_slave_encrypt(cat_sub[0], cat_sub[2]),  f'{cat_sub[1].strip()} : {cat_sub[3].strip()}') for cat_sub in categories_subcategories]
    empty_choice = [(master_slave_encrypt('00','0000'), '')]
    choices_list = [*empty_choice, *choices_list]

    incexp_header_form = Incexp_header_form()
    for position in incexp_header_form.positions:
        position.category.choices = choices_list


    return render_template("incexp/incexp_position.html.jinja", incexp_header_form=incexp_header_form)

@incexp.route('/cat-sub-options', methods=['GET'])
def get_cat_sub_options():
    type_id = request.args.get('type-id', None)
    categories_subcategories = (db.session
                                .query(Category.id,
                                        Category.name_pl,
                                        Subategory.id,
                                        Subategory.name_pl,
                                        )
                                .join(Subategory, Category.id == Subategory.category_id)
                                .filter(Category.type_id == type_id)
                                .order_by()
                            ).all()

    choices_list = [(master_slave_encrypt(cat_sub[0], cat_sub[2]),  f'{cat_sub[1].strip()} : {cat_sub[3].strip()}') for cat_sub in categories_subcategories]
    empty_choice = [(master_slave_encrypt('00','0000'), '')]
    choices_list = [*empty_choice, *choices_list, *empty_choice]

    incexp_header_form = Incexp_header_form()
    for position in incexp_header_form.positions:
        position.category.choices = choices_list

    return render_template('incexp/cat_sub_options.html.jinja', incexp_header_form=incexp_header_form)