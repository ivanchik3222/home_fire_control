from flask import Flask, render_template
from flask_login import LoginManager
import os

from analytics import get_map_analytics, get_regions_analytics
from db_models import db, User, Admin, Analytics
from admin import assigment_result, assigments_by_user_chek, create_assignment, create_object, create_user, edit_result, edit_user, send_notification
from inspection import create_form, create_result, create_ticket

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SECRET_KEY'] = os.urandom(24)

db.init_app(app)

login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    if not user_id or user_id == "None":
        return None
    return User.query.get(int(user_id)) or Admin.query.get(int(user_id))

login_manager.init_app(app)
login_manager.login_view = "login"

from auth import register, login, logout  


@app.route('/')
def index():
    return render_template('index.html')


#роуты для системы поьзователей
app.add_url_rule('/auth/register', view_func=register, methods=['POST', 'GET'])
app.add_url_rule('/auth/login', view_func=login, methods=['POST', 'GET'])
app.add_url_rule('/auth/logout', view_func=logout, methods=['GET'])


#роуты для системы администраторов
#создание чего-либо
app.add_url_rule('/admin/user/create', view_func=create_user, methods=['POST', 'GET'])
app.add_url_rule('/admin/object/create', view_func=create_object, methods=['POST', 'GET'])
app.add_url_rule('/admin/assignment/create', view_func=create_assignment, methods=['POST', 'GET'])
app.add_url_rule('/admin/notification/send', view_func=send_notification, methods=['POST'])
#просмотр чего-либо
app.add_url_rule('/admin/user/<int:user_id>/assignments', view_func=lambda user_id: assigments_by_user_chek(user_id), endpoint='lambda1', methods=['GET'])
app.add_url_rule('/admin/assigment/<int:assigment_id>/result', view_func=lambda assigment_id: assigment_result(assigment_id), endpoint='lambda2', methods=['GET'])
#изменение чего-либо
app.add_url_rule('/admin/assigment/<int:assigment_id>/edit', view_func=lambda assigment_id: edit_result(assigment_id), endpoint='lambda3', methods=['PUT'])
app.add_url_rule('/admin/user/<int:user_id>/edit', view_func=lambda user_id: edit_user(user_id), endpoint='lambda4', methods=['PUT'])


#роуты для аналитики
app.add_url_rule('/analytics/regions', view_func=get_regions_analytics, methods=['GET'])
app.add_url_rule('/analytics/fire_risk_map', view_func=get_map_analytics, methods=['GET'])


#роуты для inspection
app.add_url_rule('/inspection/ticket/create', view_func=create_ticket, methods=['POST'])
app.add_url_rule('/inspection/form/create', view_func=create_form, methods=["POST"])
app.add_url_rule('/inspection/result/create', view_funk=create_result, methods=["POST"])

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
