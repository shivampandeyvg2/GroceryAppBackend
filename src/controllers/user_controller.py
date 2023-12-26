from flask import request, Response, json, Blueprint, jsonify

from src.models.cart import cart
from src.models.user_model import User
from src.models.product_model import Product
from src import bcrypt, db
from datetime import datetime
import jwt
import os

users = Blueprint("users", __name__)

# route for signup api/users/signup
@users.route('/signup', methods = ["POST"])
def handle_signup():
    try:
        data = request.json
        if "userid" and  "name" and  "email" and "password" in data:
            user = User.query.filter_by(userid = data["userid"]).first()
            if not user:

                user_obj = User(
                    name = data["name"],
                    userid = data["userid"],
                    email = data["email"],
                    password = bcrypt.generate_password_hash(data['password']).decode('utf-8'),
                    usertype =0
                )

                db.session.add(user_obj)
                db.session.commit()

                payload = {
                    'iat': datetime.utcnow(),
                    'userid': user_obj.userid,
                    'name': user_obj.name,
                    'email': user_obj.email,
                    'usertype' : 'user'
                }
                token = jwt.encode(payload,os.getenv('SECRET_KEY'),algorithm='HS256')
                return Response(
                response=json.dumps({'status': "success",
                                    "message": "User Sign up Successful",
                                    "token": token}),
                status=201,
                mimetype='application/json'
            )
            else:
                print(user)
                return Response(
                response=json.dumps({'status': "failed", "message": "User already exists kindly use sign in"}),
                status=409,
                mimetype='application/json'
            )
        else:
            # if request parameters are not correct
            return Response(
                response=json.dumps({'status': "failed", "message": "Compolsoury User Parameters  are required"}),
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

# route for login api/users/signin
@users.route('/signin', methods = ["POST"])
def handle_login():
    try:
        data = request.json
        if "userid" and "password" in data:
            user = User.query.filter_by(userid = data["userid"] , usertype =0).first()
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
                                                "message": "User Sign In Successful",
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
                    response=json.dumps({'status': "failed", "message": "User Record doesn't exist, kindly register"}),
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



@users.route('/getproducts/<int:id>', methods = ["GET"])
def getproductsbyid(id):
    try:
        existing = Product.query.filter_by(category=id).all()
        print(existing)
        data = []
        for item in existing:
            temp = {
                "id": item.id,
                "name": item.name,
                "createdon": item.createdon,
                "unit": item.unit,
                "rate": item.rate,
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
        print(e)
        db.session.rollback()
        return Response(
            response=json.dumps({'status': "failed",
                                 "message": "Error Occured",
                                 "error": str(e)}),
            status=500,
            mimetype='application/json'
        )

@users.route('/addtocart/<userid>', methods = ["POST"])
def addtocart(userid):
    try:
        data = request.json
        print(data)
        if "productid" and "qty" and "price" in data:
           np = cart(
               user = userid,
               productid = data['productid'],
               qty = data['qty'],
               total = data['total']
           )
           db.session.add(np)
           db.session.commit()
           return Response(
            response=json.dumps({'status': "succss",
                                 }),
            status=200,
            mimetype='application/json'
        )
        return Response(
            response=json.dumps({'status': "failure",
                                 }),
            status=400,
            mimetype='application/json'
        )


    except Exception as e:
        print(e)
        db.session.rollback()
        return Response(
            response=json.dumps({'status': "failed",
                                 "message": "Error Occured",
                                 "error": str(e)}),
            status=500,
            mimetype='application/json'
        )

@users.route('/viewcart/<userid>', methods = ["GET"])
def viewcart(userid):
    try:
        car = cart.query.filter_by(user = userid).all()
        data =[]
        for c in car:
            p = Product.query.filter_by(id = c.productid).first()
            ndata ={
                "id": c.id,
                "createdon" : c.createdon,
                "productid" : c.productid,
                "qty" : c.qty,
                "total" : c .total,
                "productname" : p.name
            }
            data.append(ndata)


        print(data)

        return Response(
        response=json.dumps({'status': "succss", "data": data
                             }),
        status=200,
        mimetype='application/json'
    )

    except Exception as e:
        print(e)
        db.session.rollback()
        return Response(
            response=json.dumps({'status': "failed",
                                 "message": "Error Occured",
                                 "error": str(e)}),
            status=500,
            mimetype='application/json'
        )


