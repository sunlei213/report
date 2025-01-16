from app import db

class ProductGroup(db.Model):
    """产品组别模型"""
    __tablename__ = 'product_groups'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    order = db.Column(db.Integer, default=0)  # 排序字段
    
    # 关联
    products = db.relationship('Product', back_populates='group')
    targets = db.relationship('GroupTarget', back_populates='product_group')

class Product(db.Model):
    """产品模型"""
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50), nullable=False, unique=True)
    name = db.Column(db.String(100), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('product_groups.id'), nullable=False)
    min_amount = db.Column(db.Numeric(18, 2), default=0)  # 计算户数的最小金额
    
    # 关联
    group = db.relationship('ProductGroup', back_populates='products')

class GroupTarget(db.Model):
    """产品组对应每个客户经理的目标"""
    __tablename__ = 'group_targets'
    
    id = db.Column(db.Integer, primary_key=True)
    manager_id = db.Column(db.Integer, db.ForeignKey('managers.id'), nullable=False)
    product_group_id = db.Column(db.Integer, db.ForeignKey('product_groups.id'), nullable=False)
    target = db.Column(db.Numeric(18, 2), nullable=False)  # 目标金额
    year = db.Column(db.Integer, nullable=False)  # 年份
    
    # 关联
    manager = db.relationship('Manager', back_populates='targets')
    product_group = db.relationship('ProductGroup', back_populates='targets')
    
    # 联合唯一约束
    __table_args__ = (
        db.UniqueConstraint('manager_id', 'product_group_id', 'year', 
                          name='uk_manager_product_group_year'),
    ) 