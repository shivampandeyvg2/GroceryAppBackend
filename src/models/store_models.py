from datetime import datetime

from src import db

class Store(db.Model):
    id = db.Column(db.Integer(), primary_key = True, unique=True , autoincrement = True)
    createdby = db.Column(db.String(), nullable =False)
    storename = db.Column(db.String(60))
    isactive = db.Column(db.Integer, default =1)
    createdon = db.Column(db.DateTime, default=datetime.now())
