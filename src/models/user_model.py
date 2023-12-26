from datetime import datetime

from src import db

class User(db.Model):
    id = db.Column(db.Integer(), primary_key = True, unique=True , autoincrement=True)
    userid = db.Column(db.String(), nullable =False, unique=True)
    name = db.Column(db.String(60))
    email = db.Column(db.String(60))
    usertype = db.Column(db.Integer, nullable = False)
    isactive = db.Column(db.Integer, default =1)
    storeid = db.Column(db.Integer, default =-1)
    createdon = db.Column(db.DateTime, default=datetime.now())
    password = db.Column(db.String(80))
