from flask import Flask, flash, jsonify, redirect, render_template, request, url_for
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from db_models import db, User, Order, Admin, Analytics



def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == 'POST':
        full_name = request.form['full_name']
        password = request.form['password']
        role = request.form['role']
        login = request.form['login']

        if User.query.filter_by(login=login).first() or Admin.query.filter_by(login=login).first():
            flash('Пользователь с таким логином уже существует!', 'danger')
            return redirect(url_for('register'))

        password_hash = generate_password_hash(password)

        if role == 'user':
            user = User(full_name=full_name, password_hash=password_hash, login = login)
            db.session.add(user)
            login_user(user)
        elif role == 'admin':
            admin = Admin(full_name=full_name, password_hash=password_hash,)
            db.session.add(admin)
            login_user(admin)
        else:
            flash('Ошибка: неверная роль!', 'danger')
            return redirect(url_for('register'))

        db.session.commit()
        flash('Регистрация успешна!', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')


def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == 'POST':
        full_name = request.form['full_name']
        password = request.form['password']

        user = User.query.filter_by(full_name=full_name).first()
        admin = Admin.query.filter_by(full_name=full_name).first()

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