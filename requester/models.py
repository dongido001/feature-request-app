from flask import Flask, session
from requester import db
from datetime import date
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(128))

    def __init__(self, username=None, password=None):
        self.username = username
        self.password = generate_password_hash(password)

    def is_authenticated(self):
        return session.get('logged', False)

    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.id
    
    def check_password_hash(self, password):
        return check_password_hash(self.password, password)

    def is_anonymous(self):
        return False

    def __repr__(self):
        return '<User %r>' % (self.username)

class Client(db.Model):
    __tablename__ = 'clients'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60))

    def __init__(self, name):
        self.name = name
    
    def __repr__(self):
        return '<Client %r>' % (self.name)

class ProductCategory(db.Model):
    __tablename__ = 'product_categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<ProductCategory %r>' % (self.name)

class Request(db.Model):
    __tablename__ = 'requests'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('product_categories.id'), nullable=False)
    priority = db.Column(db.Integer, nullable=False)
    target_date = db.Column(db.Date(), default=date)

    def __repr__(self):
        return '<Request %r>' % (self.title)