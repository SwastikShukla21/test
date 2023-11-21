from config import cache
from models import *
from sqlalchemy.orm import joinedload
from config import app as a


@cache.cached(timeout=1, key_prefix="get_products")
def get_products():
    with a.app_context():
        products = db.session.query(Product).options(
            joinedload(Product.section)).all()

    print("hii")
    return products


@cache.memoize(timeout=10)
def get_transactions(order_id):
    with a.app_context():
        transactions = Transaction.query.filter_by(order_id=order_id).all()
    return transactions


@cache.cached(timeout=5)
def get_orders():
    with a.app_context():
        o = Order.query.all()
    return o


@cache.cached(timeout=5)
def get_categories():
    with a.app_context():
        o = Category.query.all()
    return o

