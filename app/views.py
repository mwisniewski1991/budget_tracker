from flask import Blueprint, render_template, request
from . import db
from .models import INCEXP, Category, Subategory, Type

views = Blueprint ('views', __name__)
ADDED_IDS = []

@views.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html')

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

        amount = float(request.form['amount']) * 100

        new_incexp = INCEXP(
                date=request.form['date'],
                type_id=request.form['type_id'],
                category_id=request.form['category'],
                subcategory_id=request.form['subcategory'],
                amount=amount,
                comment=request.form['comment'],
                shop=request.form['shop'],
                connection=request.form['connection'],
        )


        db.session.add(new_incexp)
        db.session.commit()

        ADDED_IDS.append({
            'id': new_incexp.id,
            'type_id': new_incexp.type_id,
            'category_id': new_incexp.category_id,
            'subcategory_id': new_incexp.subcategory_id,
            'amount': new_incexp.amount / 100,
        })

        feedback = f"Dodano: {request.form['category']}, {request.form['subcategory']} na kwotę: {amount / 100}. ID: {new_incexp.id}"

        print(ADDED_IDS)

        return render_template("add.html", 
                                is_added=True, 
                                types=types, categories=categories, subcategories=subcategories,
                                feedback = feedback, 
                                new_incexp = ADDED_IDS
                                )
    

    
    return render_template("add.html", is_added=False, types=types, categories=categories, subcategories=subcategories)
    


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


@views.route('/categories', methods=['GET'])
def get_categories():

    user_type_id = request.args['type_id']

    categories = Category.query.filter_by(type_id=user_type_id).order_by(Category.id).all()

    return [
        {
            'id':cat.id,
            'name_pl':cat.name_pl,
        } for cat in categories
    ]


@views.route('/subcategories', methods=['GET'])
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