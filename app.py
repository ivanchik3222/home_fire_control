from flask import Flask, render_template
from flask_login import LoginManager
import os

from db_models import db, User, Admin
from routes.auth import auth_bp
from routes.admin import admin_bp
from routes.analytics import analytics_bp
from routes.inspection import inspection_bp


login_manager = LoginManager()
app = Flask(__name__)


    
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SECRET_KEY'] = os.urandom(24)

# Регистрация блюпринтов
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(analytics_bp, url_prefix='/analytics')
app.register_blueprint(inspection_bp, url_prefix='/inspection')

# Инициализация базы данных
db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = "login"


    
@login_manager.user_loader
def load_user(user_id):
    if not user_id or user_id == "None":
        return None
    return User.query.get(int(user_id)) or Admin.query.get(int(user_id))

    
@app.route('/')
def index():
    return render_template('table.html')


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)