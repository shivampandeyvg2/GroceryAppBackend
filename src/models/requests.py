from datetime import datetime

from src import db

class ApprovalRequests(db.Model):
    id = db.Column(db.Integer(), primary_key = True, unique=True , autoincrement=True)
    requestedby = db.Column(db.String(), nullable =False)
    approvalstatus = db.Column(db.Integer, default =1)
    filename = db.Column(db.String)
    requestedon =  db.Column(db.DateTime, default=datetime.now())
    type = db.Column (db.Integer)

