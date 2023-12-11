from flask import Blueprint, render_template, request, send_from_directory, redirect
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
    categories = [
        {
            'id':cat.id,
            'name_pl':cat.name_pl,
        } for cat in Category.query.all()]

    types = [
        {
            'id':type.id,
            'name_pl':type.name_pl,

        } for type in Type.query.all()]

    subcategories = [
        {
            'id':subcat.id,
            'name_pl':subcat.name_pl,
        } for subcat in Subategory.query.all()]
    
    if request.method == "POST":
        # print(request.form)

        header_date = request.form['date']
        header_owner_id = request.form['owner_id']
        header_account_id = request.form['account_id']
        header_type_id = request.form['type_id']

        position_category = request.form['category_1']
        position_subcategory = request.form['subcategory_1']
        position_amount = request.form['amount_1']
        position_comment = request.form['comment_1']
        position_shop = request.form['shop_1']
        position_connection = request.form['connection_1']
        

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
        #         category_id=request.form['category'],
        #         subcategory_id=request.form['subcategory'],
        #         amount=amount,
        #         comment=request.form['comment'],
        #         shop=request.form['shop'],
        #         connection=request.form['connection'],


    
        # ADDED_IDS.append({
        #     'id': new_incexp.id,
        #     'type_id': new_incexp.type_id,
        #     'category_id': new_incexp.category_id,
        #     'subcategory_id': new_incexp.subcategory_id,
        #     'amount': new_incexp.amount / 100,
        # })

        # feedback = f"Dodano: {request.form['category']}, {request.form['subcategory']} na kwotę: {amount / 100}. ID: {new_incexp.id}"

        # print(ADDED_IDS)

        # return render_template("add.html", 
        #                         is_added=True, 
        #                         types=types, categories=categories, subcategories=subcategories,
        #                         feedback = feedback, 
        #                         new_incexp = ADDED_IDS
        #                         )
    

    
    # return render_template("add.html", is_added=False, types=types, categories=categories, subcategories=subcategories)
    


    # return {
    #     'date': request.form['date'],
    #     'event_type': request.form['event_type'],
    #     'category': request.form['category'],
    #     'subcategory': request.form['subcategory'],
    #     'amount': request.form['amount'],
    #     'comment': request.form['comment'],
    #     'shop': request.form['shop'],
    #     'connection': request.form['connection'],
    # }


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

@views.route('/testdb', methods=['GET'])
def testdb():
    events = INCEXP.query.all()
    results = [
        {   
            'id':event.id, 
            'date': event.date,
            'event_type': event.event_type,
            'category': event.category,
            'subcategory': event.subcategory,
            'amount': event.amount,
            'comment': event.comment,
            'shop': event.shop,
            'connection': event.connection,
        } for event in events
    ]
    return {
        'INCEXP':results
    }