from flask import Blueprint, render_template, request
from . import db
from .models import INCEXP

views = Blueprint ('views', __name__)

@views.route('/', methods=['GET'])
def home():
    return render_template("home.html")


@views.route('/aboutme', methods=['GET'])
def about_me():
    return render_template("about_me.html")

@views.route('/create_events', methods=['POST'])
def create_events():
    print(request.form['date'])
    print(request.form['event_type'])
    print(request.form['category'])
    print(request.form['subcategory'])
    print(request.form['amount'])

    return {
        'date': request.form['date'],
        'event_type': request.form['event_type'],
        'category': request.form['category'],
        'subcategory': request.form['subcategory'],
        'amount': request.form['amount'],
        'comment': request.form['comment'],
        'shop': request.form['shop'],
        'connection': request.form['connection'],
    }

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