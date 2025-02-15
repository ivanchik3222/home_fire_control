from flask import Flask, flash, jsonify, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import datetime

from db_models import db, User, Order, Admin, Analytics
from login_manager import register, login, logout

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SECRET_KEY'] = 'supersecretkey'


db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    if not user_id or user_id == "None":
        return None
    return User.query.get(int(user_id)) or Admin.query.get(int(user_id))


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/orders', methods=['GET'])
def get_orders():
    orders = Order.query.all()
    result = []
    for order in orders:
        result.append({
            'id': order.id,
            'inspector': order.inspector.full_name if order.inspector else 'Не назначен',
            'admin': order.admin.full_name,
            'address': order.address,
            'visit_time': order.visit_time.strftime('%Y-%m-%d %H:%M:%S'),
            'family_size': order.family_size,
            'family_status': order.family_status,
            'safety_status': 'Безопасно' if order.safety_status else 'Опасно'
        })
    return jsonify(result)



@app.route('/create_order', methods=['GET','POST'])
def create_order():
    if request.method == 'POST':
        address = request.form['address']
        visit_time = datetime.datetime.strptime(request.form['visit_time'], '%Y-%m-%dT%H:%M')
        family_size = int(request.form['family_size'])
        family_status = request.form['family_status']
        admin = Admin.query.first()
        if admin is None:
            return 'Error: admin not found', 500
        order = Order(address=address, visit_time=visit_time, family_size=family_size, family_status=family_status, admin_id=admin.id)
        db.session.add(order)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('create_order.html')

@app.route('/admins', methods=['GET'])
def get_admins():
    admins = Admin.query.all()
    result = []
    for admin in admins:
        result.append({
            'id': admin.id,
            'full_name': admin.full_name
        })
    return jsonify(result)

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    result = []
    for user in users:
        result.append({
            'id': user.id,
            'full_name': user.full_name
        })
    return jsonify(result)

app.add_url_rule('/register', view_func=register, methods=['POST', 'GET'])
app.add_url_rule('/login', view_func=login, methods=['POST', 'GET'])
app.add_url_rule('/logout', view_func=logout, methods=['GET'])


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
