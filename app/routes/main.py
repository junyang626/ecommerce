"""
主页路由 & 管理后台
"""
from flask import Blueprint, render_template, redirect, url_for, flash, request, g
from flask_login import login_required, current_user
from app import db
from app.models import Category, Product, Order

main_bp = Blueprint('main', __name__)


@main_bp.before_app_request
def load_categories():
    """每个请求前加载分类到全局变量"""
    g.categories = Category.query.all()


@main_bp.route('/')
def index():
    """首页：展示推荐商品"""
    categories = Category.query.all()
    products = Product.query.order_by(Product.created_at.desc()).limit(8).all()
    return render_template('index.html', categories=categories, products=products)


# ============================================================
# 管理后台（管理员权限）
# ============================================================
def admin_required(f):
    """管理员权限装饰器"""
    from functools import wraps
    @wraps(f)
    @login_required
    def decorated(*args, **kwargs):
        if not current_user.is_admin:
            flash('需要管理员权限。', 'danger')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated


@main_bp.route('/admin/products')
@admin_required
def admin_products():
    """商品管理页面"""
    products = Product.query.order_by(Product.created_at.desc()).all()
    categories = Category.query.all()
    return render_template('admin/products.html', products=products, categories=categories)


@main_bp.route('/admin/products/add', methods=['POST'])
@admin_required
def admin_product_add():
    """添加商品"""
    name = request.form.get('name', '').strip()
    price = float(request.form.get('price', 0))
    stock = int(request.form.get('stock', 0))
    category_id = int(request.form.get('category_id', 0))
    description = request.form.get('description', '').strip()
    image_url = request.form.get('image_url', '').strip()

    if not name or price <= 0:
        flash('商品名称和价格必须填写正确。', 'danger')
    else:
        product = Product(
            name=name, price=price, stock=stock,
            category_id=category_id, description=description,
            image_url=image_url or 'https://placehold.co/400x400?text=No+Image'
        )
        db.session.add(product)
        db.session.commit()
        flash(f'商品「{product.name}」添加成功！', 'success')

    return redirect(url_for('main.admin_products'))


@main_bp.route('/admin/products/edit/<int:product_id>', methods=['POST'])
@admin_required
def admin_product_edit(product_id):
    """编辑商品"""
    product = Product.query.get_or_404(product_id)
    product.name = request.form.get('name', product.name).strip()
    product.price = float(request.form.get('price', product.price))
    product.stock = int(request.form.get('stock', product.stock))
    product.category_id = int(request.form.get('category_id', product.category_id))
    product.description = request.form.get('description', '').strip()
    image_url = request.form.get('image_url', '').strip()
    if image_url:
        product.image_url = image_url
    db.session.commit()
    flash(f'商品「{product.name}」更新成功！', 'success')
    return redirect(url_for('main.admin_products'))


@main_bp.route('/admin/products/delete/<int:product_id>', methods=['POST'])
@admin_required
def admin_product_delete(product_id):
    """删除商品"""
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    flash(f'商品「{product.name}」已删除。', 'info')
    return redirect(url_for('main.admin_products'))


@main_bp.route('/admin/orders')
@admin_required
def admin_orders():
    """订单管理页面"""
    orders = Order.query.order_by(Order.created_at.desc()).all()
    return render_template('admin/orders.html', orders=orders)


@main_bp.route('/admin/orders/status/<int:order_id>', methods=['POST'])
@admin_required
def admin_order_status(order_id):
    """更新订单状态"""
    order = Order.query.get_or_404(order_id)
    new_status = request.form.get('status')
    if new_status in Order.STATUS_LABELS:
        order.status = new_status
        db.session.commit()
        flash(f'订单 #{order.id} 状态已更新为「{order.status_label}」', 'success')
    return redirect(url_for('main.admin_orders'))
