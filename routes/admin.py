import datetime
from flask import Flask, flash, jsonify, redirect, render_template, request, url_for, Blueprint
from flask_login import current_user, login_required
from werkzeug.security import generate_password_hash

from db_models import Inspection_assigment, Inspection_form, Inspection_object, Inspection_result, Inspection_ticket, Notification, db, User, Admin



admin_bp = Blueprint('admin', __name__)


def create_user():
    full_name = request.json['full_name']
    password = request.json['password']
    login = request.json['login']
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
    

@login_required
def create_object():
    if not current_user.is_authenticated:
        flash('Вы не зарегистрированы', 'danger')
        return redirect(url_for('index'))

    user_is_not_admin = User.query.filter_by(login=current_user.login).first()
    if user_is_not_admin:
        flash('Вы не администратор.', 'danger')
        return redirect(url_for('index'))

    if request.method == 'POST':
        address = request.form.get('address')
        coordinates = request.form.get('coordinates')
        obj_type  = request.form.get('type')
        obj = Inspection_object(address=address, coordinates=coordinates, type=obj_type)
        db.session.add(obj)
        db.session.commit()
        flash('Объект успешно добавлен!', 'success')
        return render_template('create_object.html')

    return render_template("create_object.html")

@login_required
def create_assignment():
    if not current_user.is_authenticated:
        flash('Вы не зарегистрированы', 'danger')
        return redirect(url_for('index'))

    user_is_not_admin = User.query.filter_by(login=current_user.login).first()
    if user_is_not_admin:
        flash('Вы не администратор.', 'danger')
        return redirect(url_for('index'))

    if request.method == 'POST':
        user_id = request.form.get('user_id')
        object_id = request.form.get('object_id')
        assignment = Inspection_assigment(user_id=user_id, object_id=object_id, admin_id=current_user.id, status="pending")
        db.session.add(assignment)
        db.session.commit()
        flash('Назначение успешно создано!', 'success')
        return render_template('create_assignment.html')

    return render_template("create_assignment.html")

def assigments_by_user_chek(user_id):
    if not current_user.is_authenticated:
        flash('Вы не зарегестррированны', 'danger')
        return redirect(url_for('index'))
    
    user_is_not_admin = User.query.filter_by(login=current_user.login).first()

    if user_is_not_admin:        
        flash('Вы не администратор.', 'danger')
        return redirect(url_for('index'))

    assignments = Inspection_assigment.query.filter_by(user_id=user_id).all()
    return render_template('assignments.html', assignments=assignments)

def assigment_result(assigment_id):
    if not current_user.is_authenticated:
        flash('Вы не зарегестррированны', 'danger')
        return redirect(url_for('index'))
    
    user_is_not_admin = User.query.filter_by(login=current_user.login).first()

    if user_is_not_admin:        
        flash('Вы не администратор.', 'danger')
        return redirect(url_for('index'))
    
    assigment = Inspection_assigment.query.filter_by(id=assigment_id).first()
    ticket = Inspection_ticket.query.filter_by(assigment_id=assigment_id).first()
    form = Inspection_form.query.filter_by(assigment_id=assigment_id).first()
    result = Inspection_result.query.filter_by(assigment_id=assigment_id).first()

    returned_json = {
        "ticket": {"inspection_date": ticket.inspection_date, "family_size": ticket.family_sizey},
        "form": form.answers,
        "result": {"fire_risk_level":result.fire_risk_level}
    }

    return jsonify(returned_json)

def edit_result(assigment_id):
    if not current_user.is_authenticated:
        flash('Вы не зарегестррированны', 'danger')
        return redirect(url_for('index'))
    
    user_is_not_admin = User.query.filter_by(login=current_user.login).first()

    if user_is_not_admin:        
        flash('Вы не администратор.', 'danger')
        return redirect(url_for('index'))
    
    if request.method == 'PUT':
        fire_risk_level = request.form['fire_risk_level']

        result = Inspection_result.query.filter_by(assigment_id=assigment_id).first()
        result.fire_risk_level = fire_risk_level
        db.session.commit()

        return jsonify({"message": "Данные успешно обновлены"}), 200
    
    return jsonify({"message": "не тот метод бро"}), 405


def edit_user(user_id):
    if not current_user.is_authenticated:
        flash('Вы не зарегестррированны', 'danger')
        return redirect(url_for('index'))
    
    user_is_not_admin = User.query.filter_by(login=current_user.login).first()

    if user_is_not_admin:
        flash('Вы не администратор.', 'danger')
        return redirect(url_for('index'))


    if request.method == 'PUT':
        full_name = request.form['full_name']
        password = request.form['password']
        login = request.form['login']

        user_exist = User.query.filter_by(login=login).first()
        admin_exist = Admin.query.filter_by(login=login).first()

        if user_exist or admin_exist:
            flash('Пользователь с таким логином уже существуует', 'danger')
            return redirect('/admin/user/create')
        
        password_hash = generate_password_hash(password)

        user = User.query.filter_by(id=user_id).first()

        user.login = login
        user.password = password_hash
        user.full_name = full_name

        db.session.commit()
        flash('Изменения сохранены', 'success')
        return redirect(url_for('index'))
        
    return render_template("change_user_data.html")

def send_notification():
    if not current_user.is_authenticated:
        flash('Вы не зарегестррированны', 'danger')
        return redirect(url_for('index'))
    
    user_is_not_admin = User.query.filter_by(login=current_user.login).first()

    if user_is_not_admin:
        flash('Вы не администратор.', 'danger')
        return redirect(url_for('index'))

    if request.method == 'POST':
        message = request.form['message']
        user_id = request.form['user_id']
        type = request.form['type']
        created_at = datetime.now()

        notification = Notification(user_id=user_id, admin_id=current_user.id, message=message, is_read = False, type=type, created_at=created_at)

        db.session.add(notification)
        db.session.commit()

        flash('Уведомление успешно отправлено', 'success')
        return redirect(url_for('index'))
    
@login_required
def admin_panel():
    if not current_user.is_authenticated:
        flash('Вы не зарегистрированы', 'danger')
        return redirect(url_for('index'))
    # Проверяем, что текущий пользователь — администратор
    admin = Admin.query.filter_by(login=current_user.login).first()
    if not admin:
        flash('Вы не администратор.', 'danger')
        return redirect(url_for('index'))
    # Получаем всех пользователей, зарегистрированных этим администратором
    users = User.query.filter_by(admin_id=current_user.id).all()
    data = []
    for user in users:
        # Количество выполненных назначений
        completed_count = Inspection_assigment.query.filter_by(user_id=user.id, status="completed").count()
        # Количество активных назначений (pending или in_progress)
        active_count = Inspection_assigment.query.filter(
            Inspection_assigment.user_id == user.id,
            Inspection_assigment.status.in_(["pending", "in_progress"])
        ).count()
        data.append({
            "user": user,
            "completed": completed_count,
            "active": active_count
        })
    # Передаем список пользователей с подсчитанными данными в шаблон
    return render_template('table.html', data=data)

# Создание чего-либо
admin_bp.add_url_rule('/user/create', view_func=create_user, methods=['POST'])
admin_bp.add_url_rule('/object/create', view_func=create_object, methods=['POST', 'GET'])
admin_bp.add_url_rule('/assignment/create', view_func=create_assignment, methods=['POST', 'GET'])
admin_bp.add_url_rule('/notification/send', view_func=send_notification, methods=['POST'])

# Просмотр
admin_bp.add_url_rule('/main', view_func=admin_panel, methods=['GET'])
admin_bp.add_url_rule('/user/<int:user_id>/assignments', view_func=assigments_by_user_chek, methods=['GET'])
admin_bp.add_url_rule('/assigment/<int:assigment_id>/result', view_func=assigment_result, methods=['GET'])

# Изменение
admin_bp.add_url_rule('/assigment/<int:assigment_id>/edit', view_func=edit_result, methods=['PUT'])
admin_bp.add_url_rule('/user/<int:user_id>/edit', view_func=edit_user, methods=['PUT'])