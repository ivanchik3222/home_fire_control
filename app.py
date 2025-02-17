from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
import os

from db_models import db, User, Admin, Analytics
from admin import assigments_chek, create_assignment, create_object, create_user

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SECRET_KEY'] = os.urandom(24)

db.init_app(app)

login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    if not user_id or user_id == "None":
        return None
    return User.query.get(int(user_id)) or Admin.query.get(int(user_id))

login_manager.init_app(app)
login_manager.login_view = "login"

from auth import register, login, logout  


@app.route('/')
def index():
    return render_template('index.html')


#роуты для системы поьзователей
app.add_url_rule('/auth/register', view_func=register, methods=['POST', 'GET'])
app.add_url_rule('/auth/login', view_func=login, methods=['POST', 'GET'])
app.add_url_rule('/auth/logout', view_func=logout, methods=['GET'])

#роуты для системы администраторов
app.add_url_rule('/admin/user/create', view_func=create_user, methods=['POST', 'GET'])
app.add_url_rule('/admin/object/create', view_func=create_object, methods=['POST', 'GET'])
app.add_url_rule('/admin/assignment/create', view_func=create_assignment, methods=['POST', 'GET'])
app.add_url_rule('/admin/user/<int:user_id>/assignments', view_func=lambda user_id: assigments_chek(user_id), endpoint='lambda1', methods=['GET'])

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
