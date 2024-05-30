from . import db 
from sqlalchemy.sql import func, text
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
import marshmallow as ma
from datetime import datetime

class Owners(db.Model):
    __tablename__ = 'owners'
    id = db.Column(db.Integer, primary_key=True)
    name_pl = db.Column(db.String(50))
    accounts = db.relationship("Accounts", backref="owners", single_parent=True, order_by="asc(Accounts.id)")

class Accounts(db.Model):
    __tablename__ = 'accounts'
    id = db.Column(db.String(2), primary_key=True, server_default=text("lpad(nextval('accounts_id_seq_custom')::text, 2, '0')"))
    name_pl = db.Column(db.String(50))
    owner_id =db.Column(db.Integer, db.ForeignKey('owners.id'))

class Type(db.Model):
    __tablename__ = 'type_dict'

    id = db.Column(db.Integer, primary_key=True)
    name_eng = db.Column(db.String(50), nullable=False)
    name_pl = db.Column(db.String(50), nullable=False)
    
class Category(db.Model):
    __tablename__ = 'category'

    id = db.Column(db.String(2), nullable=False, primary_key=True)
    name_pl = db.Column(db.String(100), nullable=False)
    type_id = db.Column(db.Integer, db.ForeignKey('type_dict.id'))
    
class Subategory(db.Model):
    __tablename__ = 'subcategory'

    id = db.Column(db.String(4), nullable=False, primary_key=True)
    name_pl = db.Column(db.String(100), nullable=False)
    category_id = db.Column(db.String(2), db.ForeignKey('category.id'), nullable=False)
    is_fixed_cost = db.Column(db.Integer, nullable=False)

class INCEXP_header(db.Model):
    __tablename__ = 'incexp_header'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime(timezone=True), nullable=False)
    source = db.Column(db.String(100))
    type_id = db.Column(db.Integer, db.ForeignKey(Type.id), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('owners.id'), nullable=False)
    account_id = db.Column(db.String(2), db.ForeignKey('accounts.id'), nullable=False)
    incexp_positions = db.relationship("INCEXP_position", backref="incexp_header", single_parent=True, order_by="asc(INCEXP_position.position_id)")
    
    type = db.relationship('Type', foreign_keys='INCEXP_header.type_id')

class INCEXP_position(db.Model):
    __tablename__ = 'incexp_position'

    header_id = db.Column(db.Integer, db.ForeignKey('incexp_header.id'), primary_key=True, )
    position_id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.String(2), db.ForeignKey(Category.id), nullable=False)
    subcategory_id = db.Column(db.String(2), db.ForeignKey(Subategory.id), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    amount_absolute = db.Column(db.Float, db.Computed("abs(amount)"))
    amount_full = db.Column(db.Integer, db.Computed("amount * 100"), nullable=False)
    comment = db.Column(db.String(200))
    connection = db.Column(db.String(100))
    created_at_cet = db.Column(db.DateTime(), server_default=func.now())
    created_at_utc = db.Column(db.DateTime(), server_default=text("(now() at time zone 'utc')"))
    updated_at_cet = db.Column(db.DateTime(), server_default=func.now())
    updated_at_utc = db.Column(db.DateTime(), server_default=text("(now() at time zone 'utc')"))

    category = db.relationship("Category",foreign_keys='INCEXP_position.category_id')
    subcategory = db.relationship("Subategory",foreign_keys='INCEXP_position.subcategory_id')



class AccountsSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Accounts
        load_instance = True
        include_fk = True

class OwnersSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Owners
        load_instance = True
        include_relationships = True
        
    accounts = ma.fields.Nested(AccountsSchema, many=True, dump_only=True, exclude=('owner_id',))

class TypesSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Type
        load_instance = True

class CategorySchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Category
        load_instance = True
    
class SubcategorySchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Subategory
        load_instance = True