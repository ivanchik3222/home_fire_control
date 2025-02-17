from flask import Flask, flash, redirect, render_template, request, url_for
from flask_login import current_user
from werkzeug.security import generate_password_hash

from db_models import Inspection_assigment, Inspection_object, db, User, Admin

def create_user():
    if not current_user.is_authenticated:
        flash('Вы не зарегестррированны', 'danger')
        return redirect(url_for('index'))
    
    user_is_not_admin = User.query.filter_by(login=current_user.login).first()

    if user_is_not_admin:
        flash('Вы не администратор.', 'danger')
        return redirect(url_for('index'))


    if request.method == 'POST':
        full_name = request.form['full_name']
        password = request.form['password']
        login = request.form['login']
        admin_id = current_user.id

        user_exist = User.query.filter_by(login=login).first()
        admin_exist = Admin.query.filter_by(login=login).first()

        if user_exist or admin_exist:
            flash('Пользователь с таким логином уже существуует', 'danger')
            return redirect('/admin/user/create')
        
        password_hash = generate_password_hash(password)

        user = User(full_name=full_name, password_hash=password_hash, login=login, admin_id=admin_id)

        db.session.add(user)
        db.session.commit()
        flash('Регистрация успешна!', 'success')
        return redirect(url_for('index'))
        
    return render_template("create_user.html")

def create_object():
    if not current_user.is_authenticated:
        flash('Вы не зарегестррированны', 'danger')
        return redirect(url_for('index'))
    
    user_is_not_admin = User.query.filter_by(login=current_user.login).first()

    if user_is_not_admin:
        flash('Вы не администратор.', 'danger')
        return redirect(url_for('index'))

    if request.method == 'POST':
        address = request.form.get('address')
        coordinates  = request.form.get('coordinates')
        type = request.form.get('type')

        object = Inspection_object(address=address, coordinates=coordinates, type=type)

        db.session.add(object)
        db.session.commit()
        flash('Объект успешно добавлен!', 'success')
        return render_template('create_object.html')
    
    return render_template("create_object.html")

def create_assignment():
    if not current_user.is_authenticated:
        flash('Вы не зарегестррированны', 'danger')
        return redirect(url_for('index'))
    
    user_is_not_admin = User.query.filter_by(login=current_user.login).first()

    if user_is_not_admin:        
        flash('Вы не администратор.', 'danger')
        return redirect(url_for('index'))

    if request.method == 'POST':
        user_id = request.form.get('user_id')
        object_id = request.form.get('object_id')

        assignment = Inspection_assigment(user_id=user_id, object_id=object_id, admin_id=current_user.id)

        db.session.add(assignment)
        db.session.commit()
        flash('Объект успешно добавлен!', 'success')
        return render_template('create_assignment.html')

    return render_template("create_assignment.html")

def assigments_chek(user_id):
    if not current_user.is_authenticated:
        flash('Вы не зарегестррированны', 'danger')
        return redirect(url_for('index'))
    
    user_is_not_admin = User.query.filter_by(login=current_user.login).first()

    if user_is_not_admin:        
        flash('Вы не администратор.', 'danger')
        return redirect(url_for('index'))

    assignments = Inspection_assigment.query.filter_by(user_id=user_id).all()
    return render_template('assignments.html', assignments=assignments)