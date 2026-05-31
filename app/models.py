"""
数据模型：User, Category, Product, CartItem, Order, OrderItem
"""
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login_manager


# ============================================================
# User
# ============================================================
class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # 关系
    cart_items = db.relationship('CartItem', backref='user', lazy='dynamic',
                                  cascade='all, delete-orphan')
    orders = db.relationship('Order', backref='user', lazy='dynamic',
                             cascade='all, delete-orphan')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# ============================================================
# Category
# ============================================================
class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.Text, default='')

    # 关系
    products = db.relationship('Product', backref='category', lazy='dynamic')

    def __repr__(self):
        return f'<Category {self.name}>'


# ============================================================
# Product
# ============================================================
class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, default='')
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, default=0)
    image_url = db.Column(db.String(256), default='https://placehold.co/400x400?text=No+Image')
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # 关系
    cart_items = db.relationship('CartItem', backref='product', lazy='dynamic',
                                  cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Product {self.name}>'


# ============================================================
# CartItem
# ============================================================
class CartItem(db.Model):
    __tablename__ = 'cart_items'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1, nullable=False)

    @property
    def subtotal(self):
        return self.product.price * self.quantity

    def __repr__(self):
        return f'<CartItem user={self.user_id} product={self.product_id} x{self.quantity}>'


# ============================================================
# Order
# ============================================================
class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    status = db.Column(db.String(20), default='pending', nullable=False)
    total_amount = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # 关系
    items = db.relationship('OrderItem', backref='order', lazy='joined',
                             cascade='all, delete-orphan')

    STATUS_LABELS = {
        'pending': '待处理',
        'paid': '已支付',
        'shipped': '已发货',
        'delivered': '已送达',
        'cancelled': '已取消',
    }

    @property
    def status_label(self):
        return self.STATUS_LABELS.get(self.status, self.status)

    def __repr__(self):
        return f'<Order {self.id} {self.status}>'


# ============================================================
# OrderItem
# ============================================================
class OrderItem(db.Model):
    __tablename__ = 'order_items'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)  # 下单时的单价

    # 关系
    product = db.relationship('Product')

    @property
    def subtotal(self):
        return self.price * self.quantity

    def __repr__(self):
        return f'<OrderItem order={self.order_id} product={self.product_id}>'
