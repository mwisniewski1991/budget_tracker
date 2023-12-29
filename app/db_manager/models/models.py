from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, DateTime, Float

base = declarative_base()

class Owners(base):
    __tablename__ = 'owners'
    id = Column(String(2), primary_key=True)
    name_pl = Column(String(50))

class Accounts(base):
    __tablename__ = 'accounts'
    id = Column(String(2), primary_key=True)
    name_pl = Column(String(50))
    owner_id =Column(String(2))

class Type(base):
    __tablename__ = 'type_dict'

    id = Column(Integer, primary_key=True)
    name_eng = Column(String(50), nullable=False)
    name_pl = Column(String(50), nullable=False)
    
class Category(base):
    __tablename__ = 'category'

    id = Column(String(2), nullable=False, primary_key=True)
    name_pl = Column(String(100), nullable=False)
    type_id = Column(Integer, primary_key=True)
    
class Subategory(base):
    __tablename__ = 'subcategory'

    id = Column(String(4), nullable=False, primary_key=True)
    name_pl = Column(String(100), nullable=False)
    category_id = Column(String(2), nullable=False)
    is_fixed_cost =  Column(Integer, nullable=False)

class INCEXP_header(base):
    __tablename__ = 'incexp_header'

    id = Column(Integer, primary_key=True)
    date = Column(DateTime(timezone=True), nullable=False)
    type_id = Column(String(1), nullable=False)
    owner_id = Column(String(2), nullable=False)
    account_id = Column(String(2), nullable=False)

class INCEXP_position(base):
    __tablename__ = 'incexp_position'

    header_id = Column(Integer, primary_key=True)
    position_id = Column(Integer, nullable=False)
    category_id = Column(String(100), nullable=False)
    subcategory_id = Column(String(100), nullable=False)
    amount = Column(Float, nullable=False)
    amount = Column(Integer, nullable=False)
    comment = Column(String(200))
    shop = Column(String(100))
    connection = Column(String(100))