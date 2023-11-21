from flask_cors import CORS
from flask import Flask
from flask_caching import Cache
from models import *
from werkzeug.security import generate_password_hash
app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///market2.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = 'EM'
app.config['SECURITY_PASSWORD_SALT'] = "EM"
app.config['CACHE_TYPE'] = "RedisCache"
app.config['CACHE_REDIS_HOST'] = "127.0.0.1"
app.config['CACHE_PORT'] = 6379


db.init_app(app)
app.app_context().push()
db.create_all()
admin = User.query.filter_by(name='admin').first()
if admin is None:
    admin = User(name='admin',password=generate_password_hash("admin123", method="sha256"),
            role="admin", email="admin@EMarket.com")
    db.session.add(admin)
    db.session.commit()
cache = Cache(app)
smtp_server = 'smtp.gmail.com'
port = 587
smtp_username = 'swastik01cs@gmail.com'
smtp_password = 'hdqrvtnsmrbhomuf'
