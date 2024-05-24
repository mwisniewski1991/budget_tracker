from flask import Blueprint, render_template, request, send_from_directory, redirect, jsonify
from sqlalchemy import text, and_, select, func, case, alias
from . import db
from .models import INCEXP_header, INCEXP_position, Category, Subategory, Type, Owners, Accounts, OwnersSchema, AccountsSchema
from functools import reduce
from operator import add
from .incexp_modify import modify_header, modify_position
import logging

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)


views = Blueprint ('views', __name__)
ADDED_IDS = []

@views.route("/", methods=['GET', 'POST'])
def base():
    return send_from_directory('../frontend/public', 'index.html')

@views.route("/<path:path>")
def home(path):
    return send_from_directory('../frontend/public', path)

@views.route('/aboutme', methods=['GET'])
def about_me():
    return render_template("about_me.html")

@views.route('/api/v1/owners', methods=['GET'])
def get_owners():
    # owners_schema = OwnersSchema(many=True, only=('id', 'name_pl'))
    owners_schema = OwnersSchema(many=True)
    owners = Owners.query.order_by(Owners.id).all()
    return owners_schema.dump(owners)

@views.route('/api/v1/owners', methods=['POST'])
def add_owners():
    owner_id = request.form.get('owner_id', None)
    new_owner_name = request.form.get('owner_name_pl', None)

    if owner_id:
        owner_existing = Owners.query.filter_by(id = owner_id).one()
        owner_existing.name_pl = new_owner_name
    else:
        new_owner_name = request.form['owner_name']
        new_owner = Owners(name_pl=new_owner_name)
        db.session.add(new_owner)

    db.session.commit()
    return redirect('/')
    
@views.route('/api/v1/owners/<owner_id>', methods=['GET'])
def get_owner(owner_id):
    if request.method == 'GET':
        owners_schema = OwnersSchema()
        owner = Owners.query.filter_by(id = owner_id).first()
        return owners_schema.dump(owner)

@views.route('/api/v1/owners/<owner_id>/accounts', methods=['GET', 'POST'])
def get_owner_accounts(owner_id):
    if request.method == 'GET':
        owners_schema = OwnersSchema()
        owner = Owners.query.filter_by(id = owner_id).first()
        return owners_schema.dump(owner)
    
        # accounts_schema = AccountsSchema(many=True)
        # accounts = Accounts.query.filter_by(owner_id = owner_id).all()
        # return accounts_schema.dump(accounts)

    if request.method == 'POST':
        account_id = request.form.get('account_id', None)
        new_account_name = request.form.get('account_name', None)

        if account_id:
            account_existing = Accounts.query.filter_by(id = account_id).one()
            account_existing.name_pl = new_account_name
        else:
            new_account = Accounts(name_pl = new_account_name, owner_id = owner_id)
            db.session.add(new_account)

        db.session.commit()

        return redirect('/')

@views.route('/api/v1/owners/<owner_id>/accounts/<account_id>/incexp', methods=['GET'])
def get_incexp(owner_id, account_id):
    user_limit = request.args.get('limit', 50)
    type_id = request.args.get('type-id', None)
    category_id = request.args.get('category-id', None)
    subcategory_id = request.args.get('subcategory-id', None)
    comment_args = request.args.get('comment', None)
    connection_args = request.args.get('connection', None)
    source_args = request.args.get('source', None)
    date_start = request.args.get('date-start', None)
    date_end = request.args.get('date-end', None)

    headers_query = (db.session.query(INCEXP_header, Type, Owners, Accounts)
                .join(Type, INCEXP_header.type_id == Type.id)
                .join(Owners, INCEXP_header.owner_id == Owners.id)
                .join(Accounts, INCEXP_header.account_id == Accounts.id)
                .filter(and_(
                                INCEXP_header.owner_id == owner_id, 
                                INCEXP_header.account_id == account_id,
                            ))
                )
    
    if type_id and type_id != "0":
        headers_query = headers_query.filter(INCEXP_header.type_id == type_id)
    
    if source_args and source_args != '':
        headers_query = headers_query.filter(INCEXP_header.source == source_args)

    if date_start and date_start != 'undefined':
        headers_query = headers_query.filter(INCEXP_header.date >= date_start)

    if date_end and date_end != 'undefined':
        headers_query = headers_query.filter(INCEXP_header.date <= date_end)

    headers = (headers_query
                    .order_by(INCEXP_header.date.desc(), INCEXP_header.id)
                    .limit(user_limit)
            ).all()


    headers_list = [{
        'header_id': incexp_header.id,
        'header_date': incexp_header.date.strftime('%Y-%m-%d'),
        'source':  incexp_header.source.strip(),
        'type_id': type.id,
        'type_name': type.name_pl.strip(),
        'owner_id': owners.id,
        'owner_name': owners.name_pl.strip(),
        'account_id': accounts.id,
        'account_name': accounts.name_pl.strip(),
        'positions':[],
            } for incexp_header, type, owners, accounts in headers 
        ]

    header_ids = list(row['header_id'] for row in headers_list)

    positions_query = (db.session.query(INCEXP_position, Category, Subategory)
                    .join(Category, INCEXP_position.category_id == Category.id)
                    .join(Subategory, INCEXP_position.subcategory_id == Subategory.id)
                    .filter(INCEXP_position.header_id.in_(header_ids))
                    .order_by(INCEXP_position.header_id)
                )
    
    if category_id and category_id != "00":
        positions_query = positions_query.filter(INCEXP_position.category_id == category_id)
    if subcategory_id and subcategory_id != "0000":
        positions_query = positions_query.filter(INCEXP_position.subcategory_id == subcategory_id)
    if comment_args and comment_args != "":
        positions_query = positions_query.filter(INCEXP_position.comment.ilike(f'%{comment_args}%'))
    if connection_args and connection_args != "":
        positions_query = positions_query.filter(INCEXP_position.connection.ilike(f'%{connection_args}%'))

    positions = positions_query.all()

    positions_list = [{
        'header_id': position.header_id,
        'position_id': position.position_id,
        'category_id': category.id,
        'category': category.name_pl.strip(),
        'subcategory_id': subcategory.id,
        'subcategory': subcategory.name_pl.strip(),
        'amount': position.amount_absolute,
        'amount': position.amount,
        'comment': position.comment.strip(),
        'connection':position.connection.strip(),
        'updated_at_cet': position.updated_at_cet.strftime('%Y-%m-%d %H:%M'),

        } for position, category, subcategory in positions
    ]

    

    for header in headers_list:
        current_header = header['header_id']
        filtered_data = list(filter(lambda x: x['header_id'] == current_header, positions_list))
        header['positions'] = filtered_data
        header['total_amount'] = reduce(lambda a,b: a+b, [position['amount'] for position in filtered_data], 0)

    headers_list = list(filter(lambda row: (len(row['positions']) > 0), headers_list))
    return sorted(headers_list, reverse=True, key=lambda incexp: (incexp['header_date'], incexp['header_id']))

@views.route('/api/v1/owners/<owner_id>/accounts/<account_id>/incexp', methods=['POST'])
def add_incexp(owner_id, account_id):    
    if request.method == "POST":
        new_incexp_header = INCEXP_header(
                date  = request.form['date'],
                source = request.form['source'],
                owner_id = owner_id,
                account_id = account_id,
                type_id = request.form['type_id'],
        )

        db.session.add(new_incexp_header)
        db.session.commit()
        print(new_incexp_header.id)

        for i in range(1, 11):
            value = request.form.get(f'category_{i}', None)

            if value:
                new_incexp_position = INCEXP_position(
                    header_id = new_incexp_header.id,
                    position_id = i,
                    category_id = request.form[f'category_{i}'],
                    subcategory_id = request.form[f'subcategory_{i}'],
                    amount = request.form[f'amount_{i}'],
                    comment = request.form[f'comment_{i}'],
                    connection = request.form[f'connection_{i}'],
                )
                db.session.add(new_incexp_position)

        db.session.commit()
        return redirect('/')

@views.route('/api/v1/owners/<owner_id>/accounts/<account_id>/incexp/<header_id>', methods=['POST'])
def modify_incexp(owner_id, account_id, header_id):
        header_id = request.form['header_id']
        modify_header(INCEXP_header.query.filter_by(owner_id=owner_id, account_id=account_id, id=header_id).one(), request)
        
        for i in range(1,11):
            position_id = request.form.get(f'position_id_{i}', None)
            
            if position_id:
                incexp_positions = INCEXP_position.query.filter(and_(INCEXP_position.header_id == header_id, INCEXP_position.position_id == position_id)).one() 
                modify_position(incexp_positions,request, i)

        db.session.commit()
        return redirect('/')
    
@views.route('/api/v1/owners/<owner_id>/accounts/<account_id>/incexp/<header_id>', methods=['DELETE'])
def delete_incexp(owner_id, account_id, header_id):
    
    if INCEXP_header.query.filter_by(owner_id=owner_id, account_id=account_id, id=header_id).first():
        INCEXP_position.query.filter_by(header_id=header_id).delete()
        INCEXP_header.query.filter_by(id=header_id).delete()
        db.session.commit()

        return {
            'status': 'DELETED',
            'value': header_id
        }
    
    return {
            'status': 'ERROR',
        }

@views.route('/api/v1/owners-accounts-amount', methods=['GET'])
def get_owners_accounts_amount():

    results = (db.session.query(
                        INCEXP_header.owner_id, 
                        INCEXP_header.account_id, 
                        Owners.name_pl,
                        Accounts.name_pl,
                        func.sum(case(
                                (INCEXP_header.type_id == '1', INCEXP_position.amount_absolute * -1),
                                (INCEXP_header.type_id == '2', INCEXP_position.amount_absolute),
                            )),
                        func.max(INCEXP_position.updated_at_cet)
                        )
                    .join(INCEXP_position, INCEXP_header.id == INCEXP_position.header_id)
                    .join(Owners, INCEXP_header.owner_id == Owners.id)
                    .join(Accounts, INCEXP_header.account_id == Accounts.id)
                    .group_by(INCEXP_header.owner_id, INCEXP_header.account_id, Owners.name_pl, Accounts.name_pl)
                    .order_by(INCEXP_header.owner_id, INCEXP_header.account_id)
                ).all()

    unique_owners_list = sorted({ (owner_row[0], owner_row[2] ) for owner_row in results }) 

    return [
        {
            'owner_id':owner[0],
            'owner_name' : owner[1],
            'accounts' : [
                {
                    "id":  str(account[1]).strip(),
                    "name":  str(account[3]).strip(),
                    "amount_sum": account[4],
                    "last_update": str(account[5].strftime('%Y-%m-%d'))
                } for account in list(filter(lambda x: x[0] ==  owner[0], results))
            ]
        } for owner in unique_owners_list
    ]

@views.route('/api/v1/accounts', methods=['GET'])
def get_accounts():
    owner_id = request.args['owner_id']
    accounts = Accounts.query.filter_by(owner_id=owner_id).order_by(Accounts.id).all()

    return [
        {
            'id':account.id,
            'name_pl':account.name_pl
        } for account in accounts
    ]

@views.route('/api/v1/types', methods=['GET'])
def get_types():
    types = Type.query.all()
    return [
        {
            'id':type.id,
            'name_pl': type.name_pl,
        } for type in types
    ]

@views.route('/api/v1/categories', methods=['GET'])
def get_categories():

    user_type_id = request.args['type_id']

    categories = Category.query.filter_by(type_id=user_type_id).order_by(Category.id).all()

    return [
        {
            'id':cat.id,
            'name_pl':cat.name_pl,
        } for cat in categories
    ]

@views.route('/api/v1/subcategories', methods=['GET'])
def get_subcategories():

    user_type_id = request.args['category_id']
    subcategories = Subategory.query.filter_by(category_id=user_type_id).order_by(Subategory.id).all()

    return [
        {
            'id': subcat.id,
            'name_pl': subcat.name_pl,
        } for subcat in subcategories
    ]

@views.route('/api/v1/categories-subcategories', methods=['GET'])
def get_categories_subcategories():
    types_list = [
        {
            'id':type.id,
            'name_pl': type.name_pl,
        } for type in Type.query.all()]

    categories_list = [
        {
            'type_id':cat.type_id,
            'id':cat.id,
            'name_pl':cat.name_pl,
        } for cat in Category.query.order_by(Category.id).all()]

    subcategories_list = [
        {
            'category_id': subcat.category_id,
            'id': subcat.id,
            'name_pl': subcat.name_pl,
        } for subcat in Subategory.query.order_by(Subategory.id).all()]


    for category in categories_list:
        iteration_category_id = category['id']
        filterd_subcategories = filter(lambda x: x['category_id'] == iteration_category_id, subcategories_list)
        category['subcategories_list'] = list(filterd_subcategories)

    for typ in types_list:
        iteration_type_id = typ['id']
        filterd_categories = filter(lambda x: x['type_id'] == iteration_type_id, categories_list)
        typ['categories_list'] = list(filterd_categories)

    return types_list 

@views.route('/api/v1/sources', methods=['GET'])
def get_sources():
    sources = INCEXP_header.query.with_entities(INCEXP_header.source).distinct().order_by(INCEXP_header.source).all()
    return [{
            'source_name': str(source.source).strip()
        } for source in sources if str(source.source).strip() != ""
    ] 

@views.route('api/v1/accountBalance', methods=['GET'])
def get_account_balace():
    account_id = request.args['account_id']
    sql = text(f'''
        select 
            sum (amount_absolute) as amount_sum
        from incexp_view
        where account_id = '{account_id}'
    ''')
    account_balance_value = list(db.session.execute(sql))

    return {
        'account_balance': account_balance_value[0][0],
     }

