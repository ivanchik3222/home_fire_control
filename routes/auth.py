from flask import Flask, flash, jsonify, redirect, render_template, request, url_for, Blueprint
from flask_login import LoginManager, login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from db_models import db, User, Admin

login_manager = LoginManager()


auth_bp = Blueprint('auth', __name__)




def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == 'POST':
        full_name = request.form['full_name']
        password = request.form['password']
        region = request.form['region']
        login = request.form['login']
        city = request.form['city']
        address = request.form['address']

        user = User.query.filter_by(login=login).first()
        admin = Admin.query.filter_by(login=login).first()

        if user or admin:
            flash('Пользователь с таким логином уже существует!', 'danger')
            return redirect(url_for('register'))

        password_hash = generate_password_hash(password)

        admin = Admin(full_name=full_name, password_hash=password_hash, login=login, region=region, city=city, address=address)

        db.session.add(admin)

        db.session.commit()
        flash('Регистрация успешна!', 'success')
        return redirect(url_for('auth.login'))

    return render_template('register.html')


def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']

        user = User.query.filter_by(login=login).first()
        admin = Admin.query.filter_by(login=login).first()

        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            flash('Вход выполнен!', 'success')
            return redirect(url_for('index'))
        elif admin and check_password_hash(admin.password_hash, password):
            login_user(admin)
            flash('Вход выполнен!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Ошибка авторизации! Проверьте данные.', 'danger')

    return render_template('login.html')


def logout():
    if not current_user.is_authenticated:
        return redirect(url_for('index'))
    logout_user()
    flash('Вы вышли из системы.', 'info')
    return redirect(url_for('index'))



auth_bp.add_url_rule('/register', view_func=register, methods=['POST', 'GET'])
auth_bp.add_url_rule('/login', view_func=login, methods=['POST', 'GET'])
auth_bp.add_url_rule('/logout', view_func=logout, methods=['GET'])