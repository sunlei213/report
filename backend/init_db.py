from app import create_app, db
from app.models import init_db, drop_db
from app.models.manager import Manager, ManagerGroup
from app.models.product import Product, ProductGroup, GroupTarget
from app.models.transaction import Transaction
from app.models.client_relation import ClientRelation
from app.models.adjustment import Adjustment

app = create_app()

def init_database():
    """初始化数据库"""
    with app.app_context():
        # 删除所有表
        drop_db()
        
        # 创建所有表
        init_db()
        
        # 创建默认数据
        # 1. 创建默认客户经理组
        default_group = ManagerGroup(name='默认组', order=0)
        db.session.add(default_group)
        
        # 2. 创建默认产品组
        default_product_group = ProductGroup(name='默认组', order=0)
        db.session.add(default_product_group)
        
        db.session.commit()

if __name__ == '__main__':
    init_database() 