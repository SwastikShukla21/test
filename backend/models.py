from flask_sqlalchemy import SQLAlchemy
import datetime
db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(70), unique=True)
    password = db.Column(db.String())

    role = db.Column(db.String())
    orders = db.relationship('Order', lazy="subquery", backref='user')

    def __repr__(self):
        return f'{self.id}'


class Product(db.Model):
    __tablename__ = "product"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    price = db.Column(db.Float)
    expdate = db.Column(db.String, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    ms = db.Column(db.String, nullable=False)
    desc = db.Column(db.String(100))

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))

    def __repr__(self):
        return f'{self.id}'


class Category(db.Model):
    __tablename__ = "category"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    c_item = db.relationship('Product',
                             backref='section', lazy="subquery")

    def __repr__(self):
        return f'{self.name}'


class Request(db.Model):
    __tablename__ = "request"
    id = db.Column(db.Integer, primary_key=True)
    cat_id = db.Column(db.Integer)
    type = db.Column(db.String, nullable=False)
    subtype = db.Column(db.String, nullable=False)
    sectionname = db.Column(db.String)
    status = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f'{self.name}'


class Order(db.Model):
    __tablename__ = "order"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.String)
    total_value = db.Column(db.Float)
    transactions = db.relationship(
        'Transaction', lazy="subquery", backref='order')
    order_timestamp = db.Column(
        db.String)
    def __repr__(self):
        return f'{self.id}'

class Transaction(db.Model):
    __tablename__ = "transaction"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    quantity = db.Column(db.Integer)
    price = db.Column(db.Float)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))

    def __repr__(self):
        return f'{self.id}'
