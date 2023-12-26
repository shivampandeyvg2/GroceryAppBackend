from flask import request, Response, json, Blueprint, jsonify
from src import db
from src.models.category_model import Category

category = Blueprint("category", __name__)

@category.route('/admin/create', methods = ["POST"])
def create_category():
    try:
        data = request.json
        if "title" in data :
           categ_obj = Category(
               title = data['title'],
               approvalstatus = 1,
               isactive =1
              )
           if "createdby" in data:
               categ_obj.createdby = data['createdby']
           if "description" in data:
               categ_obj.description = data['description']
           db.session.add(categ_obj)
           db.session.commit()
           return Response(
               response=json.dumps({'status': "success",
                                    "message": "Category Created By admin "
                                    }),
               status=200,
               mimetype='application/json'
           )
        return Response(
            response=json.dumps({'status': "failed",
                                 "message": "Title can not be empty ",
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

@category.route('/admin/edit/<int:id>', methods = ["POST"])
def edit_category(id):
    try:
        data = request.json
        existing = Category.query.filter_by(id = id).first()
        if existing:
            if "title" in data :
               existing.title = data['title']
            if "description" in data:
                existing.description = data['description']
            db.session.commit()
            return Response(
               response=json.dumps({'status': "success",
                                    "message": "Category Edited Successfully By admin ",
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

@category.route('/admin/remove/<int:id>', methods = ["GET"])
def remove_category(id):
    try:
        existing = Category.query.filter_by(id = id).first()
        if existing:
            Category.query.filter_by(id=id).delete()
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



@category.route('/admin/view', methods = ["GET"])
def view_category():
    try:
        category = Category.query.filter_by(isactive =1)
        serialized_data = []
        for item in category:
            mydict = {
                "id": item.id,
                "title": item.title,
                "createdon": item.createdon,
                "description" : item.description
            }
            serialized_data.append(mydict)

        data = {
            "category": serialized_data,

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


@category.route('/admin/view/<id>', methods = ["GET"])
def view_one(id):
    try:
        category = Category.query.filter_by(isactive =1 , id =id ).first()
        serialized_data = []
        item = category
        mydict = {
            "id": item.id,
            "title": item.title,
            "createdon": item.createdon,
            "description" : item.description
        }
        # serialized_data.append(mydict)

        data = {
            "category":mydict

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

