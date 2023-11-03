from . import db 
from sqlalchemy.sql import func

class INCEXP(db.Model):
    __tablename__ = 'INCEXP'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime(timezone=True), nullable=False)
    event_type = db.Column(db.String(50), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    subcategory = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.String(200))
    shop = db.Column(db.String(100))
    connection = db.Column(db.String(100))
    