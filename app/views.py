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

@views.route('/api/v1/owners-accounts-amount', methods=['GET'])
def get_owners_accounts_amount():
    
    sql = text('''
        select owner, account, sum (amount) as amount_sum
        from incexp_view
        group by owner_id, owner, account_id, account
        order by owner, account
    ''')

    results = db.session.execute(sql)
    print(results)

    return [{
        "owner": str(row.owner).strip(),
        "account": str(row.account).strip(),
        "amount_sum": row.amount_sum,
        } for row in results
    ]