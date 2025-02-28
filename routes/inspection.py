from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for, Blueprint
from flask_login import current_user
from db_models import Inspection_form, Inspection_object, Inspection_result, db, User, Admin, Inspection_ticket, Inspection_assigment, Notification
from datetime import datetime

inspection_bp = Blueprint('inspection', __name__)


def create_ticket():
    if not current_user.is_authenticated:
        flash('Вы не зарегестррированны', 'danger')
        return redirect(url_for('index'))
    

    if request.method == 'POST':
        inspection_date = datetime.utcnow()
        family_size = request.form['family_size']
        resident_category = request.form['resident_category']
        assigment_id = request.form['assigment_id']
        user_id = current_user.id
        admin_id = request.form['admin_id']

        ticket = Inspection_ticket(inspection_date=inspection_date, family_size=family_size, resident_category=resident_category, admin_id=admin_id, user_id=user_id, assigment_id=assigment_id)

        assigment = Inspection_assigment.query.filter_by(id=assigment_id).first()
        assigment.status = "in_progress"

        db.session.add(ticket)

        return jsonify({"message": "Данные успешно обновлены"}), 200
    
def create_form():
    if not current_user.is_authenticated:
        flash('Вы не зарегестррированны', 'danger')
        return jsonify({"message": "Войдите в аккаунт"}), 401

    answers = request.json['answers']
    assigment_id = request.json['assigment_id']
    risk_score = request.json['risk_score']

    form = Inspection_form(answers=answers, assigment_id=assigment_id, risk_score=risk_score)
    db.session.add(form)

    return jsonify({"message": "Данные успешно обновлены"}), 200

def create_result():
    if not current_user.is_authenticated:
        flash('Вы не зарегестррированны', 'danger')
        return jsonify({"message": "Войдите в аккаунт"}), 401
    
    if request.method == 'POST':
        assigment_id = request.json["assigment_id"]
        fire_risk_level = request.json["fire_risk_level"]
        user_id = request.json["user_id"]
        admin_id = request.json["admin_id"]

        result = Inspection_result(assigment_id = assigment_id, fire_risk_level=fire_risk_level, user_id=user_id, admin_id=admin_id)

        assigment = Inspection_assigment.query.filter_by(id=assigment_id).first()
        assigment.status = "completed"

        db.session.add(result)
        db.session.commit()

        return jsonify({"message": "Данные успешно обновлены"}), 200
    
def assigments_by_user_chek(user_id):
    result_json = Inspection_assigment.query.filter_by(user_id=user_id).first()
    return jsonify(result_json)

def dashboard():
    user_id = session.get('user_id')  # Получаем ID пользователя из сессии
    if user_id:
        return render_template('user_dash.html', user_id=user_id)
    return redirect(url_for('auth.user_login'))

def notifications():
    user_id = session.get('user_id')  # Получаем ID пользователя из сессии
    if user_id:
        return render_template('notifications.html', user_id=user_id)
    return redirect(url_for('auth.user_login'))

def get_notifications():
    user_id = session.get('user_id')
    
    if not user_id:
        return redirect(url_for('auth.user_login'))

    notifications = Notification.query.filter_by(user_id=user_id).order_by(Notification.created_at.desc()).all()
    notifications_data = [
        {
            "id": n.id,
            "message": n.message,
            "created_at": n.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        }
        for n in notifications
    ]
    Notification.query.filter_by(user_id=user_id, is_read=False).update({"is_read": True})

    return jsonify({"notifications": notifications_data}), 200


def ticket_form(assigment_id):
    assigment = Inspection_assigment.query.filter_by(id=assigment_id).first()
    return render_template('tickets.html', assigment=assigment)

def way_map(assigment_id):
    assigment = Inspection_assigment.query.filter_by(id=assigment_id).first()
    object = Inspection_object.query.filter_by(id=assigment.object_id).first()
    return render_template('way_map.html', coordinates=object.coordinates)

def check_list(assigment_id):
    assigment = Inspection_assigment.query.filter_by(id=assigment_id).first()
    return render_template('check_list.html', assigment=assigment)

inspection_bp.add_url_rule('/ticket/create', view_func=create_ticket, methods=['POST'])
inspection_bp.add_url_rule('/form/create', view_func=create_form, methods=['POST'])
inspection_bp.add_url_rule('/result/create', view_func=create_result, methods=['POST'])
inspection_bp.add_url_rule('/assigment/<int:user_id>', view_func=assigments_by_user_chek, methods=['GET'])
inspection_bp.add_url_rule('/dashboard', view_func=dashboard, methods=['GET'])
inspection_bp.add_url_rule('/notifications', view_func=notifications, methods=['GET'])
inspection_bp.add_url_rule('/get_notifications', view_func=get_notifications, methods=['GET'])
inspection_bp.add_url_rule('/ticket/form/<int:assigment_id>', view_func=ticket_form, methods=['GET'])
inspection_bp.add_url_rule('/way_map/<int:assigment_id>', view_func=way_map, methods=['GET'])
inspection_bp.add_url_rule('/check_list/<int:assigment_id>', view_func=check_list, methods=['GET'])