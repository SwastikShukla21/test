
import time
import random
import celery
from flask_cors import cross_origin
from flask import request, jsonify, make_response, session
from tasks import csv_creator, catwisesales, timeseries, orderrange
from middleware import token_required, generate_order_id
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import os
import datetime
from datetime import timedelta
from functools import wraps
from models import *
from config import app, cache
from cache import *
from time import perf_counter_ns


@app.route('/slogin', methods=['POST'])
@cross_origin()
def slogin():

    auth = request.get_json()
    print(auth)
    if not auth or not auth.get('username') or not auth.get('password'):

        return make_response(jsonify({"message": "Could not verify Invalid username"}), 401)

    user = User.query.filter_by(name=auth.get('username')).first()

    if not user:

        return make_response(jsonify({"message": "User does not exist"}), 401)
    if user.role != "storem":
        return make_response(jsonify({"message": "Not a store manager Unauthorized access"}), 401)

    if check_password_hash(user.password, auth.get('password')):

        token = jwt.encode({

            'exp': datetime.datetime.now() + timedelta(minutes=30),
            'role': "storem"
        }, app.config['SECRET_KEY'], "HS256")

        return make_response(jsonify({'token': token}), 201)

    return make_response(jsonify({'message': "Incorrect Password , Try again"}), 403)


@app.route('/clogin', methods=['POST', 'GET'])
@cross_origin()
def clogin():

    auth = request.get_json()

    print(auth)
    if not auth or not auth.get('username') or not auth.get('password'):

        return make_response(jsonify({"message": "Could not verify Invalid username"}), 401)
    user = User.query.filter_by(name=auth.get('username'))\
        .first()

    if not user:

        return make_response(jsonify({"message": "User does not exist"}), 401)
    if user.role != "customer":
        return make_response(jsonify({"message": "Not a user Unauthorized acess"}), 401)

    if check_password_hash(user.password, auth.get('password')):

        token = jwt.encode({

            'exp': datetime.datetime.now() + timedelta(minutes=30),
            'role': "customer"
        }, app.config['SECRET_KEY'], "HS256")

        return make_response(jsonify({'token': token, 'username': user.name}), 201)

    return make_response(jsonify({'message': "Incorrect Password , Try again"}), 403)


@app.route('/alogin', methods=['POST'])
@cross_origin(supports_credentials=True)
def alogin():

    auth = request.get_json()
    print(auth)
    if not auth or not auth.get('username') or not auth.get('password'):

        return make_response(jsonify({"message": "Could not verify Invalid username"}), 401)

    user = User.query.filter_by(name=auth.get('username')).first()

    if not user:

        return make_response(jsonify({"message": "User does not exist"}), 401)
    if user.role != "admin":
        return make_response(jsonify({"message": "Not an admin Unauthorized access"}), 401)
    if check_password_hash(user.password, auth.get('password')):

        token = jwt.encode({

            'exp': datetime.datetime.now() + timedelta(minutes=30),
            'role': "admin"
        }, app.config['SECRET_KEY'], "HS256")

        return make_response(jsonify({'token': token}), 201)

    return make_response(jsonify({'message': "Incorrect Password , Try again"}), 403)


@app.route('/ssignup', methods=['POST'])
@cross_origin(supports_credentials=True)
def managersignup():

    data = request.get_json()

    email = data.get('email')
    name = data.get('username')
    password = data.get('password')
    user = User.query.filter_by(name=name).first()
    user = User.query.filter_by(email=email).first()
    if not user:
        user = User(
            name=name,
            email=email,
            password=generate_password_hash(password, method="sha256"),
            role="storem")
        db.session.add(user)
        db.session.commit()
        message = "Successfully registered."
        return make_response(jsonify(message), 201)
    else:
        message = "User already exists. Please Log in"
        return make_response(jsonify({"message": message}), 401)


@app.route('/signup', methods=['POST'])
@cross_origin(supports_credentials=True)
def signup():

    data = request.get_json()
    email = data.get('email')
    name = data.get('username')
    password = data.get('password')
    user = User.query.filter_by(name=name).first()
    user = User.query.filter_by(email=email).first()
    if not user:

        user = User(
            name=name,
            email=email,
            password=generate_password_hash(password, method="sha256"),
            role="customer")
        db.session.add(user)
        db.session.commit()
        message = "Successfully registered."
        return make_response(jsonify(message), 201)
    else:
        message = "User already exists. Please Log in"
        return make_response(jsonify({"message": message}), 401)


@app.route('/addsection', methods=['POST'])
@cross_origin(supports_credentials=True)
@token_required
def addsection(role):
    if role != "admin":
        return make_response('Not an admin access restricted', 401)
    data = request.get_json()

    name = data.get('name')
    print(name)

    c = Category.query.filter_by(name=name).first()
    print(c)
    if not c:
        cat = Category(name=name)
        db.session.add(cat)
        db.session.commit()
        message = "Successfully added."
        return make_response(jsonify({"message": message}), 201)
    else:
        message = "Category already exists."
        return make_response(jsonify({"message": message}), 401)


@app.route("/addproduct", methods=['POST', 'GET'])
@cross_origin(supports_credentials=True)
@token_required
def addproduct(role):

    if role != "storem":
        message = "Unauthorized access access restricted"
        return make_response(jsonify({'message': message}), 401)
    data = request.get_json()

    name = data.get('name')
    price = data.get('price')
    expdate = data.get('expdate')
    quantity = data.get('quantity')
    ms = data.get('ms')
    desc = data.get('desc')
    cat = data.get('cat')
    category = db.session.query(Category).filter(Category.name == cat).first()
    cat_id = category.id

    if not cat:

        message = "Category does not exists."

        return make_response(jsonify({"message": message}), 401)
    else:
        prod = Product(

            name=name,
            price=price,
            expdate=expdate,
            quantity=quantity,
            ms=ms,
            desc=desc,
            category_id=cat_id

        )

        db.session.add(prod)
        db.session.commit()
        message = "Successfully added."

        return make_response(jsonify({"message": message}), 201)


@app.route("/categories", methods=['GET'])
@cross_origin(supports_credentials=True)
def categories():

    cats = get_categories()

    categories = [{"id": cat.id, "name": cat.name,
                   "itemlen": len(list(cat.c_item))} for cat in cats]

    return make_response(jsonify(categories), 201)


@app.route("/getscale", methods=['GET'])
@cross_origin(supports_credentials=True)
@cache.cached(timeout=300, key_prefix="get_scale")
def getscale():
    scale = [{"id": 1, "name": "Kg"}, {"id": 2, "name": "g"}, {"id": 3, "name": "L"}, {"id": 4, "name": "ml"}, {
        "id": 5, "name": "Unit"}, {"id": 6, "name": "Dozen"}, {"id": 7, "name": "Packet"}]
    return make_response(jsonify(scale), 201)


@app.route("/getproducts", methods=['GET'])
@cross_origin(supports_credentials=True)
@cache.cached(timeout=5)
def getproducts():

    prods = get_products()

    products = [{"id": prod.id, "name": prod.name, "price": prod.price, "expdate": prod.expdate,
                 "stock": prod.quantity, "ms": prod.ms, "desc": prod.desc, "category": str(prod.section)} for prod in prods]

    return make_response(jsonify(products), 201)


@app.route("/getproduct/<int:id>", methods=['GET'])
@cross_origin(supports_credentials=True)
def getproduct(id):
    prod = Product.query.filter_by(id=id).first()
    product = {"id": prod.id, "name": prod.name, "price": prod.price, "expdate": prod.expdate,
               "quantity": prod.quantity, "ms": prod.ms, "desc": prod.desc, "category": str(prod.section)}
    return make_response(jsonify(product), 201)


@app.route("/deleteproduct/<int:id>", methods=['GET'])
@cross_origin(supports_credentials=True)
@token_required
def deleteproduct(role, id):
    if role != "storem":
        return make_response('Unauthorized access access restricted', 401)
    prod = Product.query.filter_by(id=id).first()
    db.session.delete(prod)
    db.session.commit()
    return make_response(jsonify({"message": "Successfully deleted"}), 201)


@app.route("/updateproduct/<int:id>", methods=['POST'])
@cross_origin(supports_credentials=True)
@token_required
def updateproduct(role, id):
    if role != "storem":
        return make_response(jsonify({"message": 'Unauthorized access access restricted'}), 401)
    data = request.get_json()
    prod = Product.query.filter_by(id=id).first()
    prod.name = data.get('name')
    prod.price = data.get('price')
    prod.quantity = data.get('quantity')
    cat_id = Category.query.filter_by(name=data.get('category')).first().id
    prod.category_id = cat_id
    db.session.commit()
    return make_response(jsonify({"message": "Successfully updated"}), 201)


@app.route("/deletecat/<int:id>", methods=['GET'])
@cross_origin(supports_credentials=True)
@token_required
def deletecat(role, id):
    if role != "admin":
        return make_response(jsonify({"message": 'Unauthorized access access restricted'}), 401)
    cat = Category.query.filter_by(id=id).first()
    if cat != None:
        for prod in cat.c_item:
            db.session.delete(prod)
        db.session.delete(cat)
        db.session.commit()
        return make_response(jsonify({"message": "Successfully deleted"}), 201)
    else:
        return make_response(jsonify({"message": "Category does not exist"}), 401)


@app.route("/getcategory/<int:id>", methods=['GET'])
@cross_origin(supports_credentials=True)
def getcategory(id):
    cat = Category.query.filter_by(id=id).first()
    category = {"id": cat.id, "name": cat.name}
    return make_response(jsonify(category), 201)


@app.route("/updatecat/<int:id>", methods=['POST'])
@cross_origin(supports_credentials=True)
@token_required
def updatecat(role, id):
    if role != "admin":
        return make_response(jsonify({"message": 'Unauthorized access access restricted'}), 401)
    data = request.get_json()
    print(role)
    cat = Category.query.filter_by(id=id).first()
    cat.name = data.get('name')
    db.session.commit()
    return make_response(jsonify({"message": "Successfully updated"}), 201)


@app.route("/checkout", methods=['POST'])
@cross_origin(supports_credentials=True)
def checkout():
    data = request.get_json()
    trans = data.get('cart')
    order = data.get('total')
    name = data.get('username')
    user_id = User.query.filter_by(name=name).first().id
    order_id = generate_order_id()
    for p in trans:
        q = p.get('quantity')
        i = p.get('id')
        inf = Product.query.filter(Product.id == i).first()
        a = inf.quantity
        if (a == 0):
            message = "Sorry for Inconvenience" + inf.name + "went out of stock"
            return make_response(jsonify({'message': message}), 400)
        if ((a-q) < 0):
            message = "Sorry for Inconvenience Please select less quantity of"+inf.name
            return make_response(jsonify({'message': message}), 400)
        inf.quantity = a-q

        entry = Transaction(name=p.get('name'), quantity=q, price=p.get(
            'price'), order_id=order_id, product_id=p.get('id'))

        try:
            db.session.add(entry)
            db.session.commit()
        except Exception as e:
            db.session.rollback()

            return make_response(jsonify({'message': str(e)}), 500)

    odr = Order(user_id=user_id, id=order_id, total_value=order, name=name,
                order_timestamp=datetime.datetime.now().strftime("%D %H:%M:%S"))
    try:
        db.session.add(odr)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return make_response(jsonify({'message': str(e)}), 500)
    return make_response(jsonify({'message': 'Order Placed'}), 201)


@app.route("/exportproducts", methods=['GET'])
@cross_origin(supports_credentials=True)
@token_required
def exportproducts(role):

    if role != "storem":
        return make_response(jsonify({"message": 'Unauthorized access access restricted'}), 401)
    f = os.getcwd()
    filepath = f+'\\static\products.csv'
    print()
    link = csv_creator.apply_async(args=[filepath])
    print(link.id)
    return make_response(jsonify({"task_id": link.id}), 201)


@app.route("/checkstatus/<taskid>", methods=['GET'])
@cross_origin(supports_credentials=True)
@token_required
def checkstatus(role, taskid):
    if role != "storem":
        return make_response(jsonify({"message": 'Unauthorized access access restricted'}), 401)
    task_status = csv_creator.AsyncResult(taskid).state
    filepath = 'backend/static/products.csv'
    print(task_status)
    if task_status == "PENDING":
        return make_response(jsonify({"status": 'pending'}), 201)
    if task_status == "SUCCESS":
        return make_response(jsonify({"status": 'success', 'csvlink': filepath}), 201)
    print(task_status)


@app.route('/requests', methods=['GET', 'POST', 'PUT'])
@cross_origin(supports_credentials=True)
@token_required
def requests(role):
    if request.method == 'GET':
        if role == "customer":
            return make_response(jsonify({"message": 'Unauthorized access access restricted'}), 401)
        else:
            reqs = Request.query.all()
            requests = []
            for req in reqs:
                requests.append({"id": req.id, "type": req.type, "subtype": req.subtype,
                                "sectionname": req.sectionname, "status": req.status, "cat_id": req.cat_id})
            return make_response(jsonify(requests), 201)
    if request.method == "POST":
        if role != "storem":
            return make_response(jsonify({"message": 'Unauthorized access access restricted'}), 401)
        else:
            data = request.get_json()
            print(data)
            req = Request(cat_id=data.get("id"), type=data.get('type'), subtype=data.get(
                'subtype'), sectionname=data.get('newname'), status="pending")
            db.session.add(req)
            db.session.commit()
            return make_response(jsonify({"message": "Request placed successfully"}))
    if request.method == "PUT":
        if role != "admin":
            return make_response(jsonify({"message": 'Unauthorized access access restricted'}), 401)
        else:
            data = request.get_json()
            print(data)
            req = Request.query.filter_by(id=data.get("id")).first()
            req.status = data.get('status')
            db.session.commit()
            return make_response(jsonify({"message": "Request updated successfully"}))


@app.route('/getorders', methods=['GET'])
@cross_origin(supports_credentials=True)
@token_required
def getorders(role):
    if role == "storem":
        orders = get_orders()
        orderlist = []
        orderlist = [{"id": order.id, "name": order.name, "order_value": order.total_value,
                      "order_date": order.order_timestamp[:8], "order_time":order.order_timestamp[9:18]} for order in orders]

        return make_response(jsonify(orderlist), 201)

    orders = get_orders()
    orderlist = []
    orderlist = [{"id": order.id, "name": order.name, "order_value": order.total_value,
                  "order_date": order.order_timestamp[:8], "order_time":order.order_timestamp[9:18]} for order in orders
                 if order.name == request.headers['username']]

    return make_response(jsonify(orderlist), 201)


@app.route('/gettransaction', methods=['GET'])
@cross_origin(supports_credentials=True)
@token_required
def gettransaction(role):
    order_id = request.headers['orderid']
    transactions = get_transactions(order_id)
    transactionlist = []
    transactionlist = [{"id": transaction.id, "name": transaction.name, "quantity": transaction.quantity,
                        "price": transaction.price, "value": transaction.quantity*transaction.price}
                       for transaction in transactions]

    return make_response(jsonify(transactionlist), 201)


@app.route('/summary', methods=['GET'])
@cross_origin(supports_credentials=True)
@token_required
def summary(role):
    if role != 'storem':
        return make_response(jsonify({"message": 'Unauthorized access access restricted'}), 401)
    catwisesales.apply_async()
    timeseries.apply_async()
    orderrange.apply_async()

    imgpath = "backend/static/category.jpg"
    time.sleep(1)
    return make_response(jsonify({"message": "Summary generated"}), 201)


if __name__ == "__main__":

    app.run(debug=True)
