from . import db 
from sqlalchemy.sql import func


class Owners(db.Model):
    __tablename__ = 'owners'
    id = db.Column(db.String(2), primary_key=True)
    name_pl = db.Column(db.String(50))

class Accounts(db.Model):
    __tablename__ = 'accounts'
    id = db.Column(db.String(2), primary_key=True)
    name_pl = db.Column(db.String(50))
    owner_id =db.Column(db.String(2))



class INCEXP_header(db.Model):
    __tablename__ = 'incexp_header'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime(timezone=True), nullable=False)
    type_id = db.Column(db.Integer, nullable=False)

class INCEXP_position(db.Model):
    __tablename__ = 'incexp_position'

    header_id = db.Column(db.Integer, primary_key=True)
    position_id = db.Column(db.Integer)
    category_id = db.Column(db.String(100), nullable=False)
    subcategory_id = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.String(200))
    shop = db.Column(db.String(100))
    connection = db.Column(db.String(100))

class Type(db.Model):
    __tablename__ = 'type_dict'

    id = db.Column(db.Integer, primary_key=True)
    name_eng = db.Column(db.String(50), nullable=False)
    name_pl = db.Column(db.String(50), nullable=False)

    
class Category(db.Model):
    __tablename__ = 'category'

    id = db.Column(db.String(2), nullable=False, primary_key=True)
    name_pl = db.Column(db.String(100), nullable=False)
    type_id = db.Column(db.Integer, primary_key=True)
    
class Subategory(db.Model):
    __tablename__ = 'subcategory'

    id = db.Column(db.String(4), nullable=False, primary_key=True)
    name_pl = db.Column(db.String(100), nullable=False)
    category_id = db.Column(db.String(2), nullable=False)
    is_fixed_cost =  db.Column(db.Integer, nullable=False)