from flask import Blueprint, render_template, redirect, request
from ... import db
from ...models import Category, Subategory

DEFAULT_TYPE_ID = '2'

incomes_categories = Blueprint (
                    'incomes_categories', 
                    __name__,
                    template_folder="templates",
                    static_folder="static")

@incomes_categories.route("/", methods=['GET'])
def incomes_categories_home():
    categories = Category.query.filter_by(type_id=DEFAULT_TYPE_ID).order_by(Category.id).all()
    return render_template("incomes_categories/home.html.jinja", categories=categories)

@incomes_categories.route('/', methods=['POST'])
def add_category():
    new_category_name = request.form.get('category_name_pl', None)
    new_category = Category(name_pl=new_category_name, type_id=DEFAULT_TYPE_ID)
    db.session.add(new_category)
    db.session.commit()
    return redirect('/incomes-categories')

@incomes_categories.route('/<category_id>', methods=['PUT'])
def edit_owners(owner_id):
    new_owner_name = request.form.get('owner_name_pl', None)
    owner_existing = Category.query.filter_by(id = owner_id).one()
    owner_existing.name_pl = new_owner_name

    db.session.commit()
    return render_template("owners/owners_read.html.jinja", owner=owner_existing)


@incomes_categories.route('/<category_id>/edit', methods=['GET'])
def edit_owners_html(category_id):
    category = Category.query.filter_by(id = category_id).one()
    return render_template("incomes_categories/category_edit.html.jinja", category=category)

@incomes_categories.route('/<category_id>/confirmed', methods=['GET'])
def confirmed_owners_html(category_id):
    category = Category.query.filter_by(id = category_id).one()
    return render_template("incomes_categories/category_read.html.jinja", category=category)




# SUBCATEGORY

@incomes_categories.route('/<category_id>/subcategory/<subcategory_id>/edit', methods=['GET'])
def edit_accounts_html(category_id, subcategory_id):
    subcategory = Subategory.query.filter_by(id=subcategory_id, category_id=category_id).one()
    return render_template('incomes_categories/subcategory_edit.html.jinja', subcategory=subcategory)

@incomes_categories.route('/<category_id>/subcategory/<subcategory_id>/read', methods=['GET'])
def read_account_html(category_id, subcategory_id):
    subcategory = Subategory.query.filter_by(id=subcategory_id, category_id=category_id).one()
    return render_template('incomes_categories/subcategory_read.html.jinja', subcategory=subcategory)