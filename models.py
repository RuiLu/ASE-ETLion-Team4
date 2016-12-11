from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'
    uid = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100))
    lastname = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=True)
    pwdhash = db.Column(db.String(54))
    orders = db.relationship('Order', backref='users', lazy='dynamic')

    def __init__(self, firstname, lastname, email, password):
        self.firstname = firstname.title()
        self.lastname = lastname.title()
        self.email = email.lower()
        self.set_password(password)

    def set_password(self, password):
        self.pwdhash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pwdhash, password)


class Order(db.Model):
    __tablename__ = 'orders'
    oid = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer, db.ForeignKey("users.uid"))
    type = db.Column(db.String(40))
    size = db.Column(db.Integer)
    inventory = db.Column(db.Integer)
    timestamp = db.Column(db.TIMESTAMP)

    def __init__(self, type, size, inventory, uid, timestamp):
        self.type = type.title()
        self.size = size
        self.inventory = inventory
        self.uid = uid
        self.timestamp = timestamp


class Trade(db.Model):
    __tablename__ = 'trades'
    tid = db.Column(db.Integer, primary_key=True)
    oid = db.Column(db.Integer, db.ForeignKey("orders.oid"))
    type = db.Column(db.String(40))
    price = db.Column(db.Float)
    shares = db.Column(db.Float)
    notional = db.Column(db.Float)
    status = db.Column(db.String(40))
    timestamp = db.Column(db.TIMESTAMP)

    def __init__(self, type, price, shares, notional, status, oid, timestamp):
        self.type = type.title()
        self.price = price
        self.shares = shares
        self.notional = notional
        self.status = status.title()
        self.oid = oid
        self.timestamp = timestamp