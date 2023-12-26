from datetime import datetime

from src import db

class cart(db.Model):
    id = db.Column(db.Integer(), primary_key = True, unique=True , autoincrement=True)
    createdon = db.Column(db.DateTime, default=datetime.now())
    user = db.Column(db.String,nullable = False)
    productid = db.Column(db.Integer , nullable = False)
    qty = db.Column(db.Integer , nullable = False , default = 0)
    total = db.Column(db.Integer , nullable = False , default=0)


