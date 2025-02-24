from flask import Flask, flash, jsonify, redirect, render_template, request, url_for
from flask_login import current_user
from db_models import db, User, Admin, Analytics, Region_risk_map

def get_regions_analytics():
    if not current_user.is_authenticated:
        flash('Вы не зарегестррированны', 'danger')
        return redirect(url_for('index'))
    
    user_is_not_admin = User.query.filter_by(login=current_user.login).first()

    if user_is_not_admin:
        flash('Вы не администратор.', 'danger')
        return redirect(url_for('index'))
    

    analytics = Analytics.query.all()
    return jsonify(analytics)

def get_map_analytics():
    if not current_user.is_authenticated:
        flash('Вы не зарегестррированны', 'danger')
        return redirect(url_for('index'))
    
    user_is_not_admin = User.query.filter_by(login=current_user.login).first()

    if user_is_not_admin:
        flash('Вы не администратор.', 'danger')
        return redirect(url_for('index'))
    
    map = Region_risk_map.query.all()
    return jsonify(map)