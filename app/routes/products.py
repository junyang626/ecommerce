"""
商品路由：列表、详情
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models import Product, Category, CartItem

products_bp = Blueprint('products', __name__)


@products_bp.route('/')
def index():
    """商品列表，支持按分类筛选"""
    page = request.args.get('page', 1, type=int)
    category_id = request.args.get('category', type=int)
    search = request.args.get('q', '').strip()

    query = Product.query

    # 分类筛选
    if category_id:
        category = Category.query.get_or_404(category_id)
        query = query.filter_by(category_id=category_id)
    else:
        category = None

    # 搜索
    if search:
        query = query.filter(Product.name.contains(search))

    # 分页
    pagination = query.order_by(Product.created_at.desc()).paginate(
        page=page, per_page=12, error_out=False)
    products = pagination.items

    categories = Category.query.all()

    return render_template('product_list.html',
                           products=products,
                           pagination=pagination,
                           categories=categories,
                           current_category=category,
                           search=search)


@products_bp.route('/<int:product_id>')
def detail(product_id):
    """商品详情"""
    product = Product.query.get_or_404(product_id)
    # 同分类推荐
    related = Product.query.filter(
        Product.category_id == product.category_id,
        Product.id != product.id
    ).limit(4).all()
    return render_template('product_detail.html', product=product, related=related)
