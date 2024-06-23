from flask import Blueprint, render_template, redirect, request
from ... import db
from ...models import Category, Subategory

DEFAULT_TYPE_ID = '2'

types = Blueprint (
                    'types', 
                    __name__,
                    template_folder="templates",
                    static_folder="static")

@types.route("/<type_id>/category", methods=['GET'])
def types_home(type_id):
    categories = Category.query.filter_by(type_id=type_id).order_by(Category.id).all()
    return render_template("types/home.html.jinja", type_id=type_id, categories=categories)

@types.route('/<type_id>/category', methods=['POST'])
def add_category(type_id):
    new_category_name = request.form.get('category_name_pl', None)
    new_category = Category(name_pl=new_category_name, type_id=type_id)
    db.session.add(new_category)
    db.session.commit()
    return redirect('/incomes-categories')

@types.route('/<type_id>/category/<category_id>', methods=['PUT'])
def edit_category(type_id, category_id):
    new_category_name = request.form.get('category_name_pl', None)
    category = Category.query.filter_by(id = category_id).one()
    category.name_pl = new_category_name

    db.session.commit()
    return render_template("types/category_read.html.jinja", type_id=type_id, category=category)

@types.route('/<type_id>/category/<category_id>/edit', methods=['GET'])
def edit_category_html(type_id, category_id):
    category = Category.query.filter_by(id = category_id).one()
    return render_template("types/category_edit.html.jinja", type_id=type_id, category=category)

@types.route('/<type_id>/category/<category_id>/read', methods=['GET'])
def read_category_html(type_id, category_id):
    category = Category.query.filter_by(id = category_id).one()
    return render_template("types/category_read.html.jinja", type_id=type_id, category=category)


# SUBCATEGORY
@types.route('/<type_id>/category/<category_id>/subcategory', methods=['POST'])
def add_subcategory(type_id, category_id):
    new_subcategory_name = request.form.get('new_subcategory_name', None)
    new_subcategory = Subategory(category_id=category_id, name_pl=new_subcategory_name)
    db.session.add(new_subcategory)
    db.session.commit()
    return redirect('/incomes-categories')

@types.route('/<type_id>/category/<category_id>/subcategory/<subcategory_id>', methods=['PUT'])
def edit_subcategory(type_id, category_id, subcategory_id):
    new_subcategory_name = request.form.get('subcategory_name_pl', None)
    subcategory = Subategory.query.filter_by(id=subcategory_id, category_id=category_id).one()
    subcategory.name_pl = new_subcategory_name

    db.session.commit()
    return render_template('types/subcategory_read.html.jinja', type_id=type_id, subcategory=subcategory)


@types.route('/<type_id>/category/<category_id>/subcategory/<subcategory_id>/edit', methods=['GET'])
def edit_subcategory_html(type_id, category_id, subcategory_id):
    subcategory = Subategory.query.filter_by(id=subcategory_id, category_id=category_id).one()
    return render_template('types/subcategory_edit.html.jinja', type_id=type_id, subcategory=subcategory)

@types.route('/<type_id>/category/<category_id>/subcategory/<subcategory_id>/read', methods=['GET'])
def read_subcategory_html(type_id, category_id, subcategory_id):
    subcategory = Subategory.query.filter_by(id=subcategory_id, category_id=category_id).one()
    return render_template('types/subcategory_read.html.jinja', type_id=type_id, subcategory=subcategory)
