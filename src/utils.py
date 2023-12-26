import json
import os
import uuid
import time

from werkzeug.utils import secure_filename

from src import db, bcrypt
from src.models.user_model import  User
from src.models.store_models import  Store
from src.models.requests import ApprovalRequests
from src.models.category_model import  Category


def get_unique_filename(filename):
    _, file_extension = os.path.splitext(filename)
    unique_filename = str(uuid.uuid4()) + '_' + str(int(time.time())) + file_extension
    return secure_filename(unique_filename)

def savefile(data ):
    filename = 'data.json'
    nfile = get_unique_filename(filename)
    json_data = json.dumps(data)
    nn = os.path.join(os.getenv('APPROVAL_REQUESTS') , nfile)
    print (nn)
    with open(nn, 'w') as json_file:
        json_file.write(json_data)
    return nfile

def approveaccount(req):
    try:
         nn = os.path.join(os.getenv('APPROVAL_REQUESTS'), req.filename)
         with open(nn, 'r') as json_file:
            data = json.load(json_file)
            if "userid" and "name" and "email" and "password" and "storename" in data:
                user = User.query.filter_by(userid = data["userid"]).first()
                if not user:
                    store_obj = Store(
                        createdby = data['userid'],
                        storename = data['storename']
                    )
                    db.session.add(store_obj)
                    db.session.commit()
                    storeid = store_obj.id

                    user_obj = User(
                        name = data["name"],
                        userid = data["userid"],
                        email = data["email"],
                        password = bcrypt.generate_password_hash(data['password']).decode('utf-8'),
                        usertype =1,
                        storeid = storeid
                    )

                    db.session.add(user_obj)
                    db.session.commit()
                    ApprovalRequests.query.filter_by(id = req.id).delete()
                    db.session.commit()
                    return json.dumps({'status': "success",
                                        "message": "Staff Account approved  Successful"
                                     })
                else:
                    print(user)
                    ApprovalRequests.query.filter_by(id=req.id).delete()
                    db.session.commit()
                    return json.dumps({'status': "failure",
                                       "message": "User Already Exists with given username "
                                       })

            else:
                # if request parameters are not correct
                ApprovalRequests.query.filter_by(id=req.id).delete()
                return json.dumps({'status': "failure",
                                   "message": "Parameters invalid. Request Rejected"
                                   })
    except FileNotFoundError:
        print(f"File '{req.filename}' not found.")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON in file '{req.filename}': {e}")


def approveadd(req):
    try:
        nn = os.path.join(os.getenv('APPROVAL_REQUESTS'), req.filename)
        with open(nn, 'r') as json_file:
            data = json.load(json_file)
            if "title" in data:
                categ_obj = Category(
                    title=data['title'],
                    approvalstatus=1,
                    isactive=1
                )
                if "createdby" in data:
                    categ_obj.createdby = data['createdby']
                if "description" in data:
                    categ_obj.description = data['description']
                db.session.add(categ_obj)
                db.session.commit()
                delet = ApprovalRequests.query.filter_by(id = req.id).delete()
                db.session.commit()
                return json.dumps({'status': "success",
                                   "message": "Category Approved  By admin "
                                   })

            delet = ApprovalRequests.query.filter_by(id=req.id).delete()
            db.session.commit()
            return json.dumps({'status': "failure",
                               "message": "Category Rejected  By admin, Title was empty "
                               })
    except FileNotFoundError:
        print(f"File '{req.filename}' not found.")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON in file '{req.filename}': {e}")
def approvedelete(req):
    try:
        nn = os.path.join(os.getenv('APPROVAL_REQUESTS'), req.filename)
        with open(nn, 'r') as json_file:
            data = json.load(json_file)
            existing = Category.query.filter_by(id=data['id']).first()
            if existing:
                Category.query.filter_by(id=data['id']).delete()
                db.session.commit()
                ApprovalRequests.query.filter_by(id=req.id).delete()
                db.session.commit()
                return json.dumps({'status': "success",
                                   "message": "Category removal approved  By admin "
                                   })
            ApprovalRequests.query.filter_by(id=req.id).delete()
            db.session.commit()
            return json.dumps({'status': "failure",
                               "message": "Category remvoal  Rejected  By admin, TNo such category "
                               })
    except FileNotFoundError:
        print(f"File '{req.filename}' not found.")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON in file '{req.filename}': {e}")


def approveedit(req):
    try:
        nn = os.path.join(os.getenv('APPROVAL_REQUESTS'), req.filename)
        with open(nn, 'r') as json_file:
            data = json.load(json_file)
            existing = Category.query.filter_by(id=data['id']).first()
            if existing:
                if "title" in data:
                    existing.title = data['title']
                if "description" in data:
                    existing.description = data['description']
                db.session.commit()
                delet = ApprovalRequests.query.filter_by(id=req.id).delete()
                db.session.commit()
                return json.dumps({'status': "success",
                                   "message": "Category Edit Approved  By admin "
                                   })
            delet = ApprovalRequests.query.filter_by(id=req.id).delete()
            db.session.commit()
            return json.dumps({'status': "failure",
                               "message": "Category Edit Rejected  By admin No existing category found. Create one first"
                               })
    except FileNotFoundError:
        print(f"File '{req.filename}' not found.")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON in file '{req.filename}': {e}")


def removefile(filename):
    nn = os.path.join(os.getenv('APPROVAL_REQUESTS'), filename)
    print (nn)
    os.remove(nn)


