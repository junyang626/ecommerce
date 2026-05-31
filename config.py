import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'ecommerce.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 每页商品数
    PRODUCTS_PER_PAGE = 12
