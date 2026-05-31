"""
Flask 应用工厂
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = '请先登录后再访问此页面。'
login_manager.login_message_category = 'warning'


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # 初始化扩展
    db.init_app(app)
    login_manager.init_app(app)

    # 注册蓝图
    from app.routes.auth import auth_bp
    from app.routes.main import main_bp
    from app.routes.products import products_bp
    from app.routes.cart import cart_bp
    from app.routes.orders import orders_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(main_bp)
    app.register_blueprint(products_bp, url_prefix='/products')
    app.register_blueprint(cart_bp, url_prefix='/cart')
    app.register_blueprint(orders_bp, url_prefix='/orders')

    # 创建数据库表（如果不存在）
    with app.app_context():
        from app import models  # noqa: F401
        db.create_all()

    return app
