from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'  # 设置登录页面
    
    # 注册蓝图（后续会添加）
    from app.routes import main
    app.register_blueprint(main)
    
    return app
from app.models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
