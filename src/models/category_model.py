from datetime import datetime

from src import db

class Category(db.Model):
    id = db.Column(db.Integer(), primary_key = True, unique=True , autoincrement=True)
    title = db.Column(db.String(60),nullable = False)
    createdon = db.Column(db.DateTime, default=datetime.now())
    approvalstatus =db.Column(db.Integer, default=0 )
    requestedby = db.Column(db.String())
    createdby = db.Column(db.String())
    description = db.Column(db.Text)
    isactive =  db.Column(db.Integer , default =0)


