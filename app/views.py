from flask import Blueprint, render_template, request

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

    return 'ok'