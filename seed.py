"""
种子数据：初始化数据库、创建管理员账号和示例商品
运行方式：python seed.py
"""
from app import create_app, db
from app.models import User, Category, Product

app = create_app()

with app.app_context():
    # 清空已有数据（按顺序避免外键约束）
    db.drop_all()
    db.create_all()
    print("[OK] 数据库表已创建。")

    # ---- 管理员 ----
    admin = User(username='admin', email='admin@shop.com', is_admin=True)
    admin.set_password('admin123')
    db.session.add(admin)

    # ---- 普通用户 ----
    demo = User(username='demo', email='demo@shop.com')
    demo.set_password('demo123')
    db.session.add(demo)

    # ---- 商品分类 ----
    categories = [
        Category(name='手机数码', description='手机、平板、耳机等数码产品'),
        Category(name='电脑办公', description='笔记本、台式机、办公设备'),
        Category(name='服装鞋帽', description='男装、女装、鞋类、配饰'),
        Category(name='食品饮料', description='零食、饮料、保健品'),
    ]
    db.session.add_all(categories)
    db.session.flush()  # 获得分类 ID

    # ---- 示例商品 ----
    products = [
        # 手机数码
        Product(name='iPhone 15 Pro Max', price=8999.00, stock=50,
                category_id=categories[0].id,
                description='Apple iPhone 15 Pro Max，A17 Pro 芯片，钛金属设计，4800万像素主摄。',
                image_url='https://placehold.co/400x400/333/fff?text=iPhone+15'),
        Product(name='华为 Mate 60 Pro', price=6999.00, stock=30,
                category_id=categories[0].id,
                description='华为 Mate 60 Pro，麒麟 9000S，卫星通话，超感知影像。',
                image_url='https://placehold.co/400x400/1565c0/fff?text=Mate+60'),
        Product(name='AirPods Pro 2', price=1899.00, stock=100,
                category_id=categories[0].id,
                description='Apple AirPods Pro 第二代，自适应降噪，个性化空间音频。',
                image_url='https://placehold.co/400x400/333/fff?text=AirPods+Pro'),

        # 电脑办公
        Product(name='MacBook Pro 14"', price=12999.00, stock=20,
                category_id=categories[1].id,
                description='Apple MacBook Pro 14英寸，M3 Pro 芯片，Liquid Retina XDR 显示屏。',
                image_url='https://placehold.co/400x400/333/fff?text=MacBook+Pro'),
        Product(name='ThinkPad X1 Carbon', price=9999.00, stock=15,
                category_id=categories[1].id,
                description='联想 ThinkPad X1 Carbon Gen 11，14英寸商务轻薄本。',
                image_url='https://placehold.co/400x400/1a237e/fff?text=ThinkPad'),
        Product(name='罗技 MX Master 3S', price=799.00, stock=80,
                category_id=categories[1].id,
                description='罗技 MX Master 3S 无线鼠标，MagSpeed 滚轮，8K DPI。',
                image_url='https://placehold.co/400x400/616161/fff?text=MX+Master'),

        # 服装鞋帽
        Product(name='Nike Air Force 1', price=899.00, stock=200,
                category_id=categories[2].id,
                description='Nike Air Force 1 经典小白鞋，皮革鞋面，Air 缓震。',
                image_url='https://placehold.co/400x400/fff/333?text=Air+Force+1'),
        Product(name='优衣库轻薄羽绒服', price=599.00, stock=150,
                category_id=categories[2].id,
                description='优衣库高级轻型羽绒服，轻便保暖，可收纳。',
                image_url='https://placehold.co/400x400/e53935/fff?text=UNIQLO'),
        Product(name='Levi\'s 511 牛仔裤', price=699.00, stock=120,
                category_id=categories[2].id,
                description="Levi's 511 修身直筒牛仔裤，弹性面料，舒适百搭。",
                image_url='https://placehold.co/400x400/1565c0/fff?text=511'),

        # 食品饮料
        Product(name='三只松鼠坚果礼盒', price=168.00, stock=500,
                category_id=categories[3].id,
                description='三只松鼠坚果大礼包，混合坚果 12 种，每日坚果零食。',
                image_url='https://placehold.co/400x400/ff8f00/fff?text=Snacks'),
        Product(name='星巴克咖啡豆（中度烘焙）', price=128.00, stock=200,
                category_id=categories[3].id,
                description='星巴克 Pike Place 中度烘焙咖啡豆 1kg。',
                image_url='https://placehold.co/400x400/4e342e/fff?text=Coffee'),
        Product(name='依云天然矿泉水（24瓶装）', price=59.90, stock=300,
                category_id=categories[3].id,
                description='法国依云 evian 天然矿泉水 330ml × 24 瓶。',
                image_url='https://placehold.co/400x400/29b6f6/fff?text=Evian'),
    ]
    db.session.add_all(products)
    db.session.commit()

    print("[OK] 种子数据创建完成！")
    print()
    print("=" * 50)
    print("  管理员账号：admin / admin123")
    print("  测试用户：  demo  / demo123")
    print("=" * 50)
    print()
    print("运行 python run.py 启动项目 → http://127.0.0.1:5000")
