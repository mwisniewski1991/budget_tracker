from flask import Blueprint, render_template, request, send_from_directory, redirect
from sqlalchemy import text
from . import db
from .models import INCEXP_header, INCEXP_position, Category, Subategory, Type, Owners, Accounts


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

        new_incexp_header = INCEXP_header(
                date  = request.form['date'],
                owner_id = request.form['owner_id'],
                account_id = request.form['account_id'],
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
                    shop = request.form[f'shop_{i}'],
                    connection = request.form[f'connection_{i}'],
                )
                db.session.add(new_incexp_position)

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

@views.route('/api/v1/shops', methods=['GET'])
def get_shops():
    shops = INCEXP_position.query.with_entities(INCEXP_position.shop).distinct().order_by(INCEXP_position.shop).all()
    return [{
            'shop_name': str(shop.shop).strip()
        } for shop in shops if str(shop.shop).strip() != ""
    ] 

@views.route('/api/v1/owners-accounts', methods=['GET'])
def get_owners_accounts():
    sql_query = text('''
        SELECT owner_id, owner_name_pl, account_id, account_name_pl
        FROM public.owners_accounts;    
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
        select owner, account, sum (amount_absolute) as amount_sum
        from incexp_view
        group by owner_id, owner, account_id, account
        order by owner, account
    ''')

    results = db.session.execute(sql)

    return [{
        "owner": str(row.owner).strip(),
        "account": str(row.account).strip(),
        "amount_sum": row.amount_sum,
        } for row in results
    ]

@views.route('/api/v1/positions', methods=['GET'])
def get_positions():
    user_owner_id = request.args['owner_id']
    user_account_id = request.args['account_id']

    sql_header = text(f'''
        select 
            incexp_header.id,
            incexp_header.date,
            type_dict.name_pl as type_name,
            owners.name_pl as owner_name,
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

    ''')
    sql_position = text('''
        select 
            incexp_position.header_id,
            incexp_position.position_id,
            category.name_pl as category,
            subcategory.name_pl as subcategory,
            incexp_position.amount_absolute,
            incexp_position.shop
            
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
        'type_name': header.type_name,
        'owner_name': header.owner_name,
        'account_name': header.account_name,
        'positions':[],

        } for header in headers 
        ]

    positions_list = [{
        'header_id': position.header_id,
        'position_id': position.position_id,
        'category': position.category,
        'subcategory': position.subcategory,
        'amount': position.amount_absolute,
        'shop': position.shop,

        } for position in positions
    ]

    for header in headers_list:
        current_header = header['header_id']
        filtered_data = filter(lambda x: x['header_id'] == current_header ,positions_list)
        header['positions'] = list(filtered_data)


    return sorted(headers_list, key=lambda incexp: incexp['header_date'] )

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