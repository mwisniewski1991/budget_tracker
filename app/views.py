from flask import Blueprint, render_template, request
from . import db
from .models import INCEXP

views = Blueprint ('views', __name__)
ADDED_IDS = []

@views.route('/aboutme', methods=['GET'])
def about_me():
    return render_template("about_me.html")


@views.route('/', methods=['GET', 'POST'])
def home():
    if request.method == "POST":

        amount = float(request.form['amount']) * 100

        new_incexp = INCEXP(
                date=request.form['date'],
                event_type=request.form['event_type'],
                category=request.form['category'],
                subcategory=request.form['subcategory'],
                amount=amount,
                comment=request.form['comment'],
                shop=request.form['shop'],
                connection=request.form['connection'],

        )


        db.session.add(new_incexp)
        db.session.commit()
        ADDED_IDS.append({
            'id': new_incexp.id,
            'category': new_incexp.category,
            'subcategory': new_incexp.subcategory,
            'amount': new_incexp.amount / 100,
        })

        feedback = f"Dodano: {request.form['category']}, {request.form['subcategory']} na kwotę: {amount / 100}. ID: {new_incexp.id}"

        print(ADDED_IDS)

        return render_template("home.html", 
                                is_added=True, 
                                feedback = feedback, 
                                new_incexp = ADDED_IDS
                                )
    
    return render_template("home.html", is_added=False)
    


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