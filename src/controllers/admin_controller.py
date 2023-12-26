from src.models.store_models import Store
from src.models.product_model import Product
from src.models.category_model import Category

from flask import request, Response, json, Blueprint, jsonify
from src.models.user_model import User
from src.models.requests import ApprovalRequests
from src import bcrypt, db
from datetime import datetime
import jwt
import os
from src.utils import savefile, approvedelete, approveedit, approveadd, approveaccount, removefile

admin = Blueprint("admin", __name__)

@admin.route('/signin', methods = ["POST"])
def handle_login():
    try:
        print (request)
        data = request.json
        print (data)
        if "userid" and "password" in data:
            user = User.query.filter_by(userid = data["userid"] , usertype =2).first()
            if user:
                if bcrypt.check_password_hash(user.password, data["password"]):
                    payload = {
                        'iat': datetime.utcnow(),
                        'userid': user.userid,
                        'name': user.name,
                        'email': user.email,
                        'usertype': 'user'
                    }
                    token = jwt.encode(payload, os.getenv('SECRET_KEY'), algorithm='HS256')
                    return Response(
                            response=json.dumps({'status': "success",
                                                "message": "Admin Sign In Successful",
                                                "token": token}),
                            status=200,
                            mimetype='application/json'
                        )

                else:
                    return Response(
                        response=json.dumps({'status': "failed", "message": "User Password Mistmatched"}),
                        status=401,
                        mimetype='application/json'
                    )
            else:
                return Response(
                    response=json.dumps({'status': "failed", "message": "Invalid Credentials"}),
                    status=404,
                    mimetype='application/json'
                )
        else:
            # if request parameters are not correct
            return Response(
                response=json.dumps({'status': "failed", "message": "User Parameters UserID and Password are required"}),
                status=400,
                mimetype='application/json'
            )

    except Exception as e:
        return Response(
                response=json.dumps({'status': "failed",
                                     "message": "Error Occured",
                                     "error": str(e)}),
                status=500,
                mimetype='application/json'
            )

@admin.route('/approve/<int:id>', methods = ["GET"])
def approve(id):
    try:
        req = ApprovalRequests.query.filter_by(id  = id).first()
        if req:
            type = req.type
            if type ==4:
                msg =approveaccount(req)
            elif type ==3:
                msg =approveadd(req)
            elif type ==2 :
                approveedit(req)
            else:
                msg = approvedelete(req)
            removefile(req.filename)
            return Response(
                    response=json.dumps({'status': "success",
                                        "message": msg,
                                        }),
                    status=200,
                    mimetype='application/json'
                )

        else:
            return Response(
                response=json.dumps({'status': "failed", "message": "No such pending request"}),
                status=401,
                mimetype='application/json'
            )

    except Exception as e:
        return Response(
                response=json.dumps({'status': "failed",
                                     "message": "Error Occured",
                                     "error": str(e)}),
                status=500,
                mimetype='application/json'
            )



@admin.route('/reject/<int:id>', methods = ["GET"])
def reject(id):
    try:
        req = ApprovalRequests.query.filter_by(id  = id).first()
        if req:

            removefile(req.filename)
            ApprovalRequests.query.filter_by(id=id).delete()
            db.session.commit()
            return Response(
                    response=json.dumps({'status': "success",
                                        "message": "Request rejected",
                                        }),
                    status=200,
                    mimetype='application/json'
                )

        else:
            return Response(
                response=json.dumps({'status': "failed", "message": "No such pending request"}),
                status=401,
                mimetype='application/json'
            )

    except Exception as e:
        return Response(
                response=json.dumps({'status': "failed",
                                     "message": "Error Occured",
                                     "error": str(e)}),
                status=500,
                mimetype='application/json'
            )



@admin.route('/dashboard', methods = ["GET"])
def dashboard():
    try:
        users = User.query.filter_by(isactive=1).count()
        store = Store.query.filter_by(isactive =1).count()
        products = Product.query.filter_by(active=1).count()
        categories = Category.query.filter_by(isactive=1).count()
        data ={
            "user": users,
            "stores": store,
            "products": products,
            "categories": categories
        }
        return Response(
                response=json.dumps({'status': "success",
                                    "message": "Request success",
                                     "data": data
                                    }),
                status=200,
                mimetype='application/json'
            )

    except Exception as e:
        return Response(
                response=json.dumps({'status': "failed",
                                     "message": "Error Occured",
                                     "error": str(e)}),
                status=500,
                mimetype='application/json'
            )



@admin.route('/viewrequests', methods = ["GET"])
def viewrequests():
    try:
        approval = ApprovalRequests.query.filter(ApprovalRequests.type ==4).order_by(ApprovalRequests.requestedon).all()
        others = ApprovalRequests.query.filter(ApprovalRequests.type !=4).order_by(ApprovalRequests.requestedon).all()
        serialized_data=[]
        serialized_datab =[]
        for item in approval:
            mydict ={
                "id" :item.id,
                "requestedby": item.requestedby,
                "requestedon": item.requestedon
            }
            serialized_data.append(mydict)

        for item in others:
            mydict = {
                "id": item.id,
                "requestedby": item.requestedby,
                "requestedon": item.requestedon
            }
            serialized_datab.append(mydict)
        data = {
           "approval": serialized_data,
           "others": serialized_datab
                }

        return Response(
                response=json.dumps({'status': "success",
                                    "message": "Request success",
                                     "data": data
                                    }),
                status=200,
                mimetype='application/json'
            )

    except Exception as e:
        return Response(
                response=json.dumps({'status': "failed",
                                     "message": "Error Occured",
                                     "error": str(e)}),
                status=500,
                mimetype='application/json'
            )


@admin.route('/view/<int:id>', methods = ["GET"])
def viewareq(id):
    try:
        req = ApprovalRequests.query.filter_by(id  = id).first()
        if req:
            nn = os.path.join(os.getenv('APPROVAL_REQUESTS'), req.filename)
            data ={}
            with open(nn, 'r') as json_file:
                data = json.load(json_file)
            type = req.type
            if type ==4:
                res ={
                    "acc":True,
                    "edit":False,
                    "data" : data
                }
            else :
                res = {
                    "acc": False,
                    "edit": True,
                    "data": data
                }


            return Response(
                    response=json.dumps({'status': "success",
                                        "data": res
                                        }),
                    status=200,
                    mimetype='application/json'
                )

        else:
            return Response(
                response=json.dumps({'status': "failed", "message": "No such pending request"}),
                status=401,
                mimetype='application/json'
            )

    except Exception as e:
        return Response(
                response=json.dumps({'status': "failed",
                                     "message": "Error Occured",
                                     "error": str(e)}),
                status=500,
                mimetype='application/json'
            )

