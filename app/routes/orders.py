"""
订单路由：创建、查看、详情
"""
from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models import Order, OrderItem, CartItem, Product

orders_bp = Blueprint('orders', __name__)


@orders_bp.route('/')
@login_required
def index():
    """我的订单"""
    orders = (Order.query
              .filter_by(user_id=current_user.id)
              .order_by(Order.created_at.desc())
              .all())
    return render_template('orders.html', orders=orders)


@orders_bp.route('/<int:order_id>')
@login_required
def detail(order_id):
    """订单详情"""
    order = Order.query.get_or_404(order_id)
    if order.user_id != current_user.id and not current_user.is_admin:
        flash('无权查看此订单。', 'danger')
        return redirect(url_for('orders.index'))
    return render_template('order_detail.html', order=order)


@orders_bp.route('/create', methods=['POST'])
@login_required
def create():
    """从购物车创建订单"""
    cart_items = (CartItem.query
                  .filter_by(user_id=current_user.id)
                  .join(Product)
                  .all())

    if not cart_items:
        flash('购物车是空的，请先添加商品。', 'warning')
        return redirect(url_for('cart.index'))

    # 检查库存
    for item in cart_items:
        if item.quantity > item.product.stock:
            flash(f'商品「{item.product.name}」库存不足（剩余 {item.product.stock} 件）。', 'danger')
            return redirect(url_for('cart.index'))

    # 创建订单
    total_amount = sum(item.subtotal for item in cart_items)
    order = Order(user_id=current_user.id, total_amount=total_amount)

    for item in cart_items:
        order_item = OrderItem(
            product_id=item.product_id,
            quantity=item.quantity,
            price=item.product.price  # 下单时的价格
        )
        order.items.append(order_item)
        # 扣减库存
        item.product.stock -= item.quantity

    db.session.add(order)

    # 清空购物车
    for item in cart_items:
        db.session.delete(item)

    db.session.commit()

    flash(f'订单 #{order.id} 创建成功！总金额 ¥{total_amount:.2f}。', 'success')
    return redirect(url_for('orders.detail', order_id=order.id))
