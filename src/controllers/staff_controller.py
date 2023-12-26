import base64
import io

from flask import request, Response, json, Blueprint, jsonify

from src.models.product_model import Product
from src.models.user_model import User
from src.models.store_models import Store
from src.models.requests import ApprovalRequests
from src import bcrypt, db
from datetime import datetime
import jwt
import os
from PIL import Image

from src.utils import savefile, removefile, get_unique_filename

staffs = Blueprint("staff", __name__)

# @staffs.route('/signup', methods = ["POST"])
# def handle_signup():
#     try:
#         data = request.json
#         if "userid" and  "name" and  "email" and "password"  and "storename" in data:
#             user = User.query.filter_by(userid = data["userid"]).first()
#             if not user:
#                 store_obj = Store(
#                     createdby = data['userid'],
#                     storename = data['storename']
#                 )
#                 db.session.add(store_obj)
#                 db.session.commit()
#                 storeid = store_obj.id
#
#                 user_obj = User(
#                     name = data["name"],
#                     userid = data["userid"],
#                     email = data["email"],
#                     password = bcrypt.generate_password_hash(data['password']).decode('utf-8'),
#                     usertype =1,
#                     storeid = storeid
#                 )
#
#                 db.session.add(user_obj)
#                 db.session.commit()
#
#                 payload = {
#                     'iat': datetime.utcnow(),
#                     'userid': user_obj.userid,
#                     'name': user_obj.name,
#                     'email': user_obj.email,
#                     'usertype' : 'staff'
#                 }
#                 token = jwt.encode(payload,os.getenv('SECRET_KEY'),algorithm='HS256')
#                 return Response(
#                 response=json.dumps({'status': "success",
#                                     "message": "Staff Sign up Successful",
#                                     "token": token}),
#                 status=201,
#                 mimetype='application/json'
#             )
#             else:
#                 print(user)
#                 return Response(
#                 response=json.dumps({'status': "failed", "message": "User already exists either as a staff or user. kindly use sign in"}),
#                 status=409,
#                 mimetype='application/json'
#             )
#         else:
#             # if request parameters are not correct
#             return Response(
#                 response=json.dumps({'status': "failed", "message": "Compolsoury User Parameters  are required"}),
#                 status=400,
#                 mimetype='application/json'
#             )
#
#     except Exception as e:
#         print (e)
#         db.session.rollback()
#         return Response(
#                 response=json.dumps({'status': "failed",
#                                      "message": "Error Occured",
#                                      "error": str(e)}),
#                 status=500,
#                 mimetype='application/json'
#             )

# route for login api/users/signin
@staffs.route('/signin', methods = ["POST"])
def handle_login():
    try:
        data = request.json
        if "userid" and "password" in data:
            user = User.query.filter_by(userid = data["userid"] , usertype =1).first()
            if user:
                if bcrypt.check_password_hash(user.password, data["password"]):
                    payload = {
                        'iat': datetime.utcnow(),
                        'userid': user.userid,
                        'name': user.name,
                        'email': user.email,
                        'usertype': 'staff'
                    }
                    token = jwt.encode(payload, os.getenv('SECRET_KEY'), algorithm='HS256')
                    return Response(
                            response=json.dumps({'status': "success",
                                                "message": "Staff Sign In Successful",
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
                    response=json.dumps({'status': "failed", "message": "User Record doesn't exist in staffs, kindly register"}),
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


@staffs.route('/request', methods = ["POST"])
def request_approval():
    try:
        data = request.json
        if "requestedby" and "type" in data:
            fname = savefile(data)
            nrequest = ApprovalRequests(
                requestedby = data['requestedby'],
                filename = fname,
                type  = int(data['type'])
            )
            db.session.add(nrequest)
            db.session.commit()
            return Response(
               response=json.dumps({'status': "success",
                                    "message": "Approval Request sent  ",
                                    "requestid": nrequest.id

                                    }),
               status=200,
               mimetype='application/json'
           )
        return Response(
        response=json.dumps({'status': "failed",
                             "message": "Requester unknown",
                             }),
        status=400,
        mimetype='application/json'
    )

    except Exception as e:
        print (e)
        db.session.rollback()
        return Response(
                response=json.dumps({'status': "failed",
                                     "message": "Error Occured",
                                     "error": str(e)}),
                status=500,
                mimetype='application/json'
            )



@staffs.route('/product/create', methods = ["POST"])
def create_product():
    try:
        data = request.form
        print(data)
        if "name"  and "rate" and "qty" and "createdby" in data:
            product = Product(
                name = data['name'],
                rate = data['rate'],
                qty = data['qty'],
                createdby = data["createdby"]
            )
            if "unit" in data:
                product.unit = data['unit']
            if "category" in data:
                product.category = data['category']
            if 'img' in request.files:
                file = request.files['img']
                print (file)
                if file.filename != '':
                    filename = get_unique_filename(file.filename)
                    file.save(os.path.join(os.getenv('APPROVAL_REQUESTS'), filename))
                    product.img = filename
            db.session.add(product)
            db.session.commit()
            return Response(
               response=json.dumps({'status': "success",
                                    "message": "Product added suuccessfully "

                                    }),
               status=200,
               mimetype='application/json'
           )
        return Response(
        response=json.dumps({'status': "failed",
                             "message": "Please provide required parameters",
                             }),
        status=400,
        mimetype='application/json'
    )

    except Exception as e:
        print (e)
        db.session.rollback()
        return Response(
                response=json.dumps({'status': "failed",
                                     "message": "Error Occured",
                                     "error": str(e)}),
                status=500,
                mimetype='application/json'
            )



@staffs.route('/product/edit/<int:id>', methods = ["POST"])
def edit_product(id):
    try:
        data = request.form
        existing = Product.query.filter_by(id = id).first()
        if existing:
            if "name" in data :
               existing.name = data['name']
            if "createdon" in data:
                existing.createdon = data['createdon']
            if "category" in data:
                existing.category = data['category']
            if "unit" in data:
                existing.unit = data['unit']
            if "rate" in data:
                existing.rate = data['rate']
            if "qty" in data:
                existing.qty = data['qty']
            if 'img' in request.files:
                file = request.files['img']
                if file.filename != '':
                    filename = get_unique_filename(file.filename)
                    file.save(os.path.join(os.getenv('APPROVAL_REQUESTS'), filename))
                    prevf = existing.img
                    removefile(prevf)
                    existing.img = filename

            db.session.commit()
            return Response(
               response=json.dumps({'status': "success",
                                    "message": "Product Edited Successfully By staff ",
                                    "categoryid": id

                                    }),
               status=200,
               mimetype='application/json'
           )
        return Response(
        response=json.dumps({'status': "failed",
                             "message": "No existing Product Found ",
                             }),
        status=400,
        mimetype='application/json'
    )

    except Exception as e:
        print (e)
        db.session.rollback()
        return Response(
                response=json.dumps({'status': "failed",
                                     "message": "Error Occured",
                                     "error": str(e)}),
                status=500,
                mimetype='application/json'
            )


@staffs.route('/product/remove/<int:id>', methods = ["GET"])
def remove_product(id):
    try:
        existing = Product.query.filter_by(id = id).first()
        if existing:
            fname = existing.img
            if fname:
                removefile(fname)
            Product.query.filter_by(id=id).delete()
            db.session.commit()
            return Response(
               response=json.dumps({'status': "success",
                                    "message": "Category Deleted Successfully By admin ",
                                    "categoryid": id

                                    }),
               status=200,
               mimetype='application/json'
           )
        return Response(
        response=json.dumps({'status': "failed",
                             "message": "No existing Category Found ",
                             }),
        status=400,
        mimetype='application/json'
    )

    except Exception as e:
        print (e)
        db.session.rollback()
        return Response(
                response=json.dumps({'status': "failed",
                                     "message": "Error Occured",
                                     "error": str(e)}),
                status=500,
                mimetype='application/json'
            )



@staffs.route('/product/get/<int:categid>/<userid>', methods = ["GET"])
def getproduct(categid, userid):
    try:
        existing = Product.query.filter_by(category=categid , createdby =userid).all()
        print (existing)
        data =[]
        for item in existing:
            temp ={
                "id" : item.id,
                "name" : item.name,
                "createdon": item.createdon,
                "unit":item.unit,
                "rate":item.rate,
                "qty": item.qty,
                "img": item.img
            }
            data.append(temp)

        return Response(
            response=json.dumps({'status': "succss",
                                 "data": data}),
            status=200,
            mimetype='application/json'
        )


    except Exception as e:
        print (e)
        db.session.rollback()
        return Response(
                response=json.dumps({'status': "failed",
                                     "message": "Error Occured",
                                     "error": str(e)}),
                status=500,
                mimetype='application/json'
            )

@staffs.route('/product/get/<productid>', methods = ["GET"])
def viewproduct(productid):
    try:
        existing = Product.query.filter_by(id = productid ).first()
        if existing:
            data ={}
            item = existing

            temp ={
                "id" : item.id,
                "name" : item.name,
                "createdon": item.createdon,
                "unit":item.unit,
                "rate":item.rate,
                "qty": item.qty,
                "img": item.img
            }
            data = temp


            return Response(
                response=json.dumps({'status': "succss",
                                     "data": data}),
                status=200,
                mimetype='application/json'
            )
        return Response(
            response=json.dumps({'status': "succss",
                                 "msg": "server error"}),
            status=500,
            mimetype='application/json'
        )


    except Exception as e:
        print (e)
        db.session.rollback()
        return Response(
                response=json.dumps({'status': "failed",
                                     "message": "Error Occured",
                                     "error": str(e)}),
                status=500,
                mimetype='application/json'
            )