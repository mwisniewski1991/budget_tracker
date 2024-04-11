from flask import Blueprint, render_template, request, send_from_directory, redirect
from sqlalchemy import text, and_
from . import db
from .models import INCEXP_header, INCEXP_position, Category, Subategory, Type, Owners, Accounts
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
    print(request.form)
    return send_from_directory('../frontend/public', 'index.html')

@views.route("/<path:path>")
def home(path):
    return send_from_directory('../frontend/public', path)


@views.route('/aboutme', methods=['GET'])
def about_me():
    return render_template("about_me.html")

@views.route('/add', methods=['GET', 'POST'])
def add():    
    if request.method == "POST":

        owner_id, account_id =  request.form['owner_account_ids'].split('_')

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
                    # shop = request.form[f'shop_{i}'],
                    connection = request.form[f'connection_{i}'],
                )
                db.session.add(new_incexp_position)

        db.session.commit()
        return redirect('/')

@views.route('/modify', methods=['GET', 'POST'])
def modify():
    if request.method == "POST":
        header_id = request.form['header_id']
        modify_header(INCEXP_header.query.filter_by(id=header_id).one(), request)
        
        for i in range(1,11):
            position_id = request.form.get(f'position_id_{i}', None)
            
            if position_id:
                incexp_positions = INCEXP_position.query.filter(and_(INCEXP_position.header_id == header_id, INCEXP_position.position_id == position_id)).one() 
                modify_position(incexp_positions,request, i)

        db.session.commit()
        return redirect('/')


@views.route('/api/v1/owners', methods=['GET'])
def get_owners():
    owners = Owners.query.all()
    return [
        {   
            'id':owner.id,
            'name_pl':owner.name_pl

        } for owner in owners
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

@views.route('/api/v1/owners-accounts', methods=['GET'])
def get_owners_accounts():
    sql_query = text('''
        SELECT owner_id, owner_name_pl, account_id, account_name_pl
        FROM public.owners_accounts
        ORDER BY owner_id, account_id;
        ''')
    
    owners_accounts = db.session.execute(sql_query)

    return [
        {
            'owner_id':owner_account.owner_id,
            'owner_name_pl':owner_account.owner_name_pl,
            'account_id':owner_account.account_id,
            'account_name_pl':owner_account.account_name_pl,
            
        } for owner_account in owners_accounts
    ]

@views.route('/api/v1/owners-accounts-amount', methods=['GET'])
def get_owners_accounts_amount():
    
    sql = text('''
        select 
            owner_id, 
            owner, 
            account, 
            sum (amount_absolute) as amount_sum,
            date(max(header_updated_at_cet)) as last_update
        from incexp_view
        group by owner_id, owner, account_id, account
        order by owner, account
    ''')

    results = list(db.session.execute(sql))
    owners_list = { (owner_row.owner_id, owner_row.owner ) for owner_row in results} # unique owner_id, owner

    return [{
        "owner_id": owner_id[0].strip(),
        "owner": owner,
        "owner_accounts": [
            {
                "account_name":  str(account_row.account).strip(),
                "amount_sum": account_row.amount_sum,
                "last_update": str(account_row.last_update)
            }
            for account_row in list(filter(lambda x: x.owner_id == owner_id, results))
        ],
        } for owner_id, owner in owners_list
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

@views.route('/api/v1/positions', methods=['GET'])
def get_positions():
    user_owner_id = request.args['owner_id']
    user_account_id = request.args['account_id']
    limit = request.args.get('limit', 50)

    sql_header = text(f'''
        select 
            incexp_header.id,
            incexp_header.date,
            incexp_header.source,           

            incexp_header.type_id,                                 
            type_dict.name_pl as type_name,
                      
            incexp_header.owner_id,
            owners.name_pl as owner_name,
                      
            incexp_header.account_id,
            accounts.name_pl as account_name
            
        from public.incexp_header

        left join public.type_dict as type_dict
            on incexp_header.type_id = type_dict.id
            
        left join public.owners as owners
            on incexp_header.owner_id = owners.id

        left join public.accounts as accounts  
        on incexp_header.account_id = accounts.id
                      
        where incexp_header.owner_id = '{user_owner_id}'
        and incexp_header.account_id = '{user_account_id}'

        order by incexp_header.date DESC, incexp_header.id DESC

        limit {limit}

    ''')
    sql_position = text('''
        select 
            incexp_position.header_id,
            incexp_position.position_id,
                        
            incexp_position.category_id,
            category.name_pl as category,

            incexp_position.subcategory_id,
            subcategory.name_pl as subcategory,
            
            incexp_position.amount_absolute,
            
            incexp_position.comment,
            incexp_position.connection                         
            
        from public.incexp_position as incexp_position

        left join public.category as category
            on incexp_position.category_id = category.id

        left join public.subcategory as subcategory
            on incexp_position.subcategory_id = subcategory.id
    ''')

    headers = db.session.execute(sql_header)
    positions = db.session.execute(sql_position)

    headers_list = [{
        'header_id': header.id,
        'header_date': header.date.strftime('%Y-%m-%d'),
        'source':  header.source.strip(),
        'type_id': header.type_id,
        'type_name': header.type_name.strip(),
        'owner_id': header.owner_id,
        'owner_name': header.owner_name.strip(),
        'account_id': header.account_id,
        'account_name': header.account_name.strip(),
        'positions':[],
        } for header in headers 
        ]

    positions_list = [{
        'header_id': position.header_id,
        'position_id': position.position_id,
        'category_id': position.category_id,
        'category': position.category.strip(),
        'subcategory_id': position.subcategory_id,
        'subcategory': position.subcategory.strip(),
        'amount': position.amount_absolute,
        'comment': position.comment.strip(),
        'connection':position.connection.strip(),

        } for position in positions
    ]

    for header in headers_list:
        current_header = header['header_id']
        filtered_data = list(filter(lambda x: x['header_id'] == current_header, positions_list))

        header['positions'] = filtered_data
        header['total_amount'] = reduce(lambda a,b: a+b, [position['amount'] for position in filtered_data])

    return sorted(headers_list, reverse=True, key=lambda incexp: incexp['header_date'])

@views.route('/api/v1/position-delete', methods=['DELETE'])
def delete_positions():
    header_id_to_delete = request.args['headerid']
    print(header_id_to_delete)


    INCEXP_position.query.filter_by(header_id=header_id_to_delete).delete()
    INCEXP_header.query.filter_by(id=header_id_to_delete).delete()
    db.session.commit()

    return [{
        'value':header_id_to_delete

    }]