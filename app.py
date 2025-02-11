from flask import Flask, jsonify, redirect, render_template, request, url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SECRET_KEY'] = 'supersecretkey'
db = SQLAlchemy(app)

# Модель пользователя (Пожарного)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(150), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    orders = db.relationship('Order', backref='inspector', lazy=True)

# Модель администратора
class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(150), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    orders = db.relationship('Order', backref='admin', lazy=True)

# Модель Талона (Заказа на проверку)
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    inspector_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    visit_time = db.Column(db.DateTime, nullable=False)
    family_size = db.Column(db.Integer, nullable=False)
    family_status = db.Column(db.String(100), nullable=True)
    safety_status = db.Column(db.Boolean, default=False)

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

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        full_name = request.form['full_name']
        password = request.form['password']
        role = request.form['role']
        password_hash = generate_password_hash(password)

        if role == 'user':
            user = User(full_name=full_name, password_hash=password_hash)
            db.session.add(user)
        elif role == 'admin':
            admin = Admin(full_name=full_name, password_hash=password_hash)
            db.session.add(admin)
        else:
            return 'Ошибка: неверная роль', 400
        
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        full_name = request.form['full_name']
        password = request.form['password']
        
        user = User.query.filter_by(full_name=full_name).first()
        admin = Admin.query.filter_by(full_name=full_name).first()
        
        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            session['role'] = 'user'
            return redirect(url_for('index'))
        elif admin and check_password_hash(admin.password_hash, password):
            session['admin_id'] = admin.id
            session['role'] = 'admin'
            return redirect(url_for('index'))
        else:
            return 'Ошибка авторизации!'
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('admin_id', None)
    session.pop('role', None)
    return redirect(url_for('index'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
