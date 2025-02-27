from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for, Blueprint
from flask_login import current_user
from db_models import Inspection_form, Inspection_result, db, User, Admin, Inspection_ticket, Inspection_assigment


inspection_bp = Blueprint('inspection', __name__)


def create_ticket():
    if not current_user.is_authenticated:
        flash('Вы не зарегестррированны', 'danger')
        return redirect(url_for('index'))
    
    user_is_not_admin = User.query.filter_by(login=current_user.login).first()

    if user_is_not_admin:
        flash('Вы не администратор.', 'danger')
        return redirect(url_for('index'))

    if request.method == 'POST':
        inspection_date = request.form['inspection_date']
        family_size = request.form['family_size']
        resident_category = request.form['resident_category']
        assigment_id = request.form['assigment_id']
        user_id = request.form['user_id']
        admin_id = current_user.id

        ticket = Inspection_ticket(inspection_date=inspection_date, family_size=family_size, resident_category=resident_category, admin_id=admin_id, user_id=user_id, assigment_id=assigment_id)

        assigment = Inspection_assigment.query.filter_by(id=assigment_id).first()
        assigment.status = "in_progress"

        db.session.add(ticket)
        db.session.commit()

        return jsonify({"message": "Данные успешно обновлены"}), 200
    
def create_form():
    if not current_user.is_authenticated:
        flash('Вы не зарегестррированны', 'danger')
        return redirect(url_for('index'))
    
    user_is_not_admin = User.query.filter_by(login=current_user.login).first()

    if user_is_not_admin:
        flash('Вы не администратор.', 'danger')
        return redirect(url_for('index'))

    if request.method == 'POST':
        answers = request.form['answers']
        assigment_id = request.form['assigment_id']
        risk_score = request.form['risk_score']

        form = Inspection_form(answers=answers, admin_id=current_user.id, assigment_id=assigment_id, risk_score=risk_score)
        db.session.add(form)
        db.session.commit()

        return jsonify({"message": "Данные успешно обновлены"}), 200

def create_result():
    if not current_user.is_authenticated:
        flash('Вы не зарегестррированны', 'danger')
        return redirect(url_for('index'))
    
    user_is_not_admin = User.query.filter_by(login=current_user.login).first()

    if user_is_not_admin:
        flash('Вы не администратор.', 'danger')
        return redirect(url_for('index'))

    if request.method == 'POST':
        assigment_id = request.form["assigment_id"]
        fire_risk_level = request.form["fire_risk_level"]
        user_id = request.form["user_id"]
        admin_id = current_user.id

        result = Inspection_result(assigment_id = assigment_id, fire_risk_level=fire_risk_level, user_id=user_id, admin_id=admin_id)

        db.session.add(result)
        db.commit()

        return jsonify({"message": "Данные успешно обновлены"}), 200
    
def assigments_by_user_chek(user_id):
    result_json = Inspection_assigment.query.filter_by(user_id=user_id).first()
    return jsonify(result_json)


def dashboard():
    user_id = session.get('user_id')  # Получаем ID пользователя из сессии
    return render_template('mobile.html', user_id=user_id)

def notifications():
    return render_template('notifications.html')


inspection_bp.add_url_rule('/ticket/create', view_func=create_ticket, methods=['POST'])
inspection_bp.add_url_rule('/form/create', view_func=create_form, methods=['POST'])
inspection_bp.add_url_rule('/result/create', view_func=create_result, methods=['POST'])
inspection_bp.add_url_rule('/assigment/<int:user_id>', view_func=assigments_by_user_chek, methods=['GET'])
inspection_bp.add_url_rule('/dashboard', view_func=dashboard, methods=['GET'])
inspection_bp.add_url_rule('/notifications', view_func=notifications, methods=['GET'])
