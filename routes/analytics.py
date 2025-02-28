from flask import Flask, flash, jsonify, redirect, render_template, request, url_for, Blueprint
from flask_login import current_user
from db_models import Inspection_assigment, Inspection_form, Inspection_object, db, User, Admin, Analytics, Region_risk_map


analytics_bp = Blueprint('analytics', __name__)


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


def analitics_map():
    # Проверка авторизации и прав администратора (при необходимости)
    if not current_user.is_authenticated:
        flash('Вы не зарегестрированы', 'danger')
        return redirect(url_for('index'))
    # Здесь можно добавить проверку на администратора, если нужно
    return render_template('map-1.html')



def map_data():
    objects = Inspection_object.query.all()
    markers = []
    for obj in objects:
        # Получаем назначение для объекта
        assigment = Inspection_assigment.query.filter_by(object_id=obj.id).first()
        # Получаем форму проверки, если назначение существует
        fire_form = Inspection_form.query.filter_by(assigment_id=assigment.id).first() if assigment else None

        # Разбиваем строку координат, предполагается формат "lat,lng"
        try:
            lat_str, lng_str = obj.coordinates.split(',')
            lat = float(lat_str.strip())
            lng = float(lng_str.strip())
        except ValueError:
            continue  # Если координаты заданы некорректно, пропускаем объект

        # Если форма проверки отсутствует или риск не задан – выводим "в процессе проверки"
        if fire_form is None or fire_form.risk_score is None:
            score = "в процессе проверки"
        else:
            score = fire_form.risk_score

        markers.append({
            "lat": lat,
            "lng": lng,
            "fire_score": score
        })
    return jsonify(markers)


analytics_bp.add_url_rule('/regions', view_func=get_regions_analytics, methods=['GET'])
analytics_bp.add_url_rule('/fire_risk_map', view_func=get_map_analytics, methods=['GET'])
analytics_bp.add_url_rule('/map_data', view_func=map_data, methods=["GET"])
analytics_bp.add_url_rule("/map", view_func=analitics_map, methods=["GET"])