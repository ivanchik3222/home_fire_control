from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from db_models import db, User, Admin, Analytics

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SECRET_KEY'] = 'supersecretkey'

db.init_app(app)

login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    if not user_id or user_id == "None":
        return None
    return User.query.get(int(user_id)) or Admin.query.get(int(user_id))

login_manager.init_app(app)
login_manager.login_view = "login"

from user_system import register, login, logout  




@app.route('/')
def index():
    return render_template('index.html')


#роуты для системы поьзователей
app.add_url_rule('/register', view_func=register, methods=['POST', 'GET'])
app.add_url_rule('/login', view_func=login, methods=['POST', 'GET'])
app.add_url_rule('/logout', view_func=logout, methods=['GET'])


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
