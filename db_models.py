from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(150), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    login = db.Column(db.String(150), nullable=False)
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'), nullable=True)

class Admin(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(150), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(150), nullable=False)
    region = db.Column(db.String(150))
    city = db.Column(db.String(150))
    address = db.Column(db.String(150))

class Inspection_object(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(150), nullable=False)
    coordinates = db.Column(db.String(150), nullable=False)
    type = db.Column(db.String(150), nullable=False)

class Inspection_assigment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    object_id = db.Column(db.Integer, db.ForeignKey('inspection_object.id'), nullable=False)
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'), nullable=False)
    status = db.Column(db.String(150), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)

class Inspection_ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    assigment_id = db.Column(db.Integer, db.ForeignKey('inspection_assigment.id'), nullable=False)
    inspection_date = db.Column(db.DateTime, nullable=False)
    family_size = db.Column(db.Integer, nullable=False)
    resident_category = db.Column(db.String(150), nullable=False)
    user_id =db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'), nullable=False)

class Inspection_form(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    assigment_id = db.Column(db.Integer, db.ForeignKey('inspection_assigment.id'), nullable=False)
    answers = db.Column(db.JSON, nullable=False)
    risk_score = db.Column(db.Float, nullable=False)

class Inspection_result(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    assigment_id = db.Column(db.Integer, db.ForeignKey('inspection_assigment.id'), nullable=False)
    fire_risk_level = db.Column(db.String(150), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'), nullable=False) 

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'), nullable=False)
    message = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    is_read = db.Column(db.Boolean, default=False, nullable=False)

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