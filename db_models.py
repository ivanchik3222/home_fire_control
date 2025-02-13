from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(150), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    login = db.Column(db.String(150), nullable=False)
    orders = db.relationship('Order', backref='inspector', lazy=True)


class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(150), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    orders = db.relationship('Order', backref='admin', lazy=True)


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    inspector_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    visit_time = db.Column(db.DateTime, nullable=False)
    family_size = db.Column(db.Integer, nullable=False)
    family_status = db.Column(db.String(100), nullable=True)
    safety_status = db.Column(db.Boolean, default=False)


class Analytics(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    region = db.Column(db.String(100), nullable=False)
    average_family_size = db.Column(db.Float, nullable=False)


class Region_risk_map(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    region = db.Column(db.String(100), nullable=False)
    risk_level = db.Column(db.String(100), nullable=False)


if __name__ == "__main__":
    print("wrong file bro")