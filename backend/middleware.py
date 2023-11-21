from functools import wraps
from flask import request, jsonify
import jwt
from config import app
import string
import time
import random




def prectice():
    print(request.headers)

    
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message': 'Token is missing !!'}), 401

        try:

            data = jwt.decode(
                token, app.config['SECRET_KEY'], algorithms="HS256")

            role = data['role']
            print(role)
        except:
            return jsonify({
                'message': 'Token is invalid !!'
            }), 401

        return f(role, *args, **kwargs)

    return decorated


def generate_order_id(length=8):
    timestamp = int(time.time())
    random_part = ''.join(random.choices(
        string.ascii_uppercase + string.digits, k=length - len(str(timestamp))))
    order_id = f"{timestamp}{random_part}"
    return order_id[:length]
