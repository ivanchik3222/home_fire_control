from flask import Flask, flash, redirect, render_template, request, url_for, Blueprint
from flask_login import LoginManager, login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from db_models import db, User, Admin  # Предполагается, что у вас есть модели User и Admin

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///yourdb.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.register'

auth_bp = Blueprint('auth', __name__)

@login_manager.user_loader
def load_user(user_id):
    # Пытаемся найти сначала пользователя, затем администратора
    user = User.query.get(int(user_id))
    if user:
        return user
    return Admin.query.get(int(user_id))

def register():
    if request.method == 'POST':
        full_name = request.form['full_name']
        password = request.form['password']
        region = request.form['region']
        login_val = request.form['login']
        city = request.form['city']
        address = request.form['address']

        user = User.query.filter_by(login=login_val).first()
        admin = Admin.query.filter_by(login=login_val).first()

        if user or admin:
            flash('Пользователь с таким логином уже существует!', 'danger')
            return redirect(url_for('auth.register'))

        password_hash = generate_password_hash(password)

        admin = Admin(full_name=full_name, password_hash=password_hash, login=login_val,
                      region=region, city=city, address=address)
        db.session.add(admin)
        db.session.commit()

        login_user(admin)  # Авторизуем нового пользователя

        flash('Регистрация успешна!', 'success')
        return redirect(url_for('auth.register'))  # Теперь после регистрации редиректим в панель

    return render_template('register.html')

def admin_login():
    login_val = request.form['login']
    password = request.form['password']

    admin = Admin.query.filter_by(login=login_val).first()
    if admin and check_password_hash(admin.password_hash, password):
        login_user(admin)
        flash('Вход выполнен!', 'success')
        return redirect(url_for('admin.admin_panel'))
    print('Ошибка авторизации! Проверьте данные.', 'danger')
    return redirect(url_for('auth.register'))


def user_login():
    if request.method == 'POST':
        login_val = request.form['login']
        password = request.form['password']

        user = User.query.filter_by(login=login_val).first()
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            flash('Вход выполнен!', 'success')
            return render_template('mobile.html')
        else:
            print('Ошибка авторизации! Проверьте данные.', 'danger')
    return render_template('user_login.html')

def logout():
    if not current_user.is_authenticated:
        return redirect(url_for('index'))
    logout_user()
    flash('Вы вышли из системы.', 'info')
    return redirect(url_for('index'))

# Регистрация и вход/выход для администратора (используются стандартные маршруты)
auth_bp.add_url_rule('/register', view_func=register, methods=['GET', 'POST'])
auth_bp.add_url_rule('/login', view_func=admin_login, methods=['POST'])
auth_bp.add_url_rule('/logout', view_func=logout, methods=['GET'])

# Отдельные маршруты для входа/выхода пользователя
auth_bp.add_url_rule('/user/login', view_func=user_login, methods=['GET', 'POST'])
auth_bp.add_url_rule('/user/logout', view_func=logout, methods=['GET'])

app.register_blueprint(auth_bp)

# Пример главной страницы
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
