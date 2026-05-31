"""
购物车路由：查看、添加、更新、删除
"""
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models import Product, CartItem

cart_bp = Blueprint('cart', __name__)


@cart_bp.route('/')
@login_required
def index():
    """查看购物车"""
    cart_items = (CartItem.query
                  .filter_by(user_id=current_user.id)
                  .join(Product)
                  .order_by(CartItem.id.desc())
                  .all())
    total = sum(item.subtotal for item in cart_items)
    return render_template('cart.html', cart_items=cart_items, total=total)


@cart_bp.route('/add/<int:product_id>', methods=['POST'])
@login_required
def add(product_id):
    """加入购物车"""
    product = Product.query.get_or_404(product_id)

    if product.stock <= 0:
        flash('该商品已缺货。', 'warning')
        return redirect(url_for('products.detail', product_id=product_id))

    quantity = int(request.form.get('quantity', 1))
    quantity = max(1, min(quantity, product.stock))

    # 查找已有购物车项
    cart_item = CartItem.query.filter_by(
        user_id=current_user.id, product_id=product_id
    ).first()

    if cart_item:
        cart_item.quantity = min(cart_item.quantity + quantity, product.stock)
    else:
        cart_item = CartItem(
            user_id=current_user.id,
            product_id=product_id,
            quantity=quantity
        )
        db.session.add(cart_item)

    db.session.commit()
    flash(f'「{product.name}」已加入购物车！', 'success')
    return redirect(request.referrer or url_for('products.detail', product_id=product_id))


@cart_bp.route('/update/<int:item_id>', methods=['POST'])
@login_required
def update(item_id):
    """更新购物车项数量"""
    cart_item = CartItem.query.get_or_404(item_id)

    if cart_item.user_id != current_user.id:
        flash('无权操作。', 'danger')
        return redirect(url_for('cart.index'))

    quantity = int(request.form.get('quantity', 1))
    quantity = max(1, min(quantity, cart_item.product.stock))
    cart_item.quantity = quantity
    db.session.commit()
    flash('购物车已更新。', 'success')
    return redirect(url_for('cart.index'))


@cart_bp.route('/remove/<int:item_id>', methods=['POST'])
@login_required
def remove(item_id):
    """移除购物车项"""
    cart_item = CartItem.query.get_or_404(item_id)

    if cart_item.user_id != current_user.id:
        flash('无权操作。', 'danger')
        return redirect(url_for('cart.index'))

    db.session.delete(cart_item)
    db.session.commit()
    flash('商品已从购物车移除。', 'info')
    return redirect(url_for('cart.index'))
