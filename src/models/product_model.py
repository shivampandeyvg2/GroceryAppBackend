from datetime import datetime

from src import db

class Product(db.Model):
    id = db.Column(db.Integer(), primary_key = True, unique=True , autoincrement=True)
    name = db.Column(db.String(60))
    createdon = db.Column(db.DateTime, default=datetime.now())
    category = db.Column(db.Integer , default =-1 )
    unit = db.Column(db.String(100))
    rate = db.Column(db.Integer)
    qty = db.Column(db.Integer)
    active = db.Column(db.Integer , default =1)
    img = db.Column(db.String)
    createdby = db.Column(db.String, nullable = False , default ="-1")





