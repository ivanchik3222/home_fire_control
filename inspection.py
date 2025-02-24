from flask import Flask, flash, jsonify, redirect, render_template, request, url_for
from flask_login import current_user
from db_models import Inspection_form, Inspection_result, db, User, Admin, Inspection_ticket

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