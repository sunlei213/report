from app import db
from datetime import datetime

class Adjustment(db.Model):
    """调整数据模型"""
    __tablename__ = 'adjustments'
    
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)  # 调整日期
    account = db.Column(db.String(50), nullable=False)  # 账号
    manager_id = db.Column(db.Integer, db.ForeignKey('managers.id'), nullable=False)  # 客户经理
    
    # 产品信息直接记录
    product_code = db.Column(db.String(50), nullable=False)  # 产品代码
    product_name = db.Column(db.String(100), nullable=False)  # 产品名称
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=True)  # 可选关联到产品表
    
    amount = db.Column(db.Numeric(18, 2), nullable=False)  # 调整金额(可以为负)
    reason = db.Column(db.String(200))  # 调整原因
    remark = db.Column(db.String(500))  # 备注
    serial_no = db.Column(db.String(50), unique=True)  # 流水号,用于更新数据
    
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)  # 创建时间
    updated_at = db.Column(db.DateTime, onupdate=datetime.now)  # 更新时间
    
    # 关联
    manager = db.relationship('Manager')
    product = db.relationship('Product')  # 可选关联
    
    # 索引
    __table_args__ = (
        db.Index('idx_adjustment_date', 'date'),  # 按日期查询
        db.Index('idx_adjustment_account', 'account'),  # 按账号查询
        db.Index('idx_adjustment_product', 'product_code'),  # 按产品查询
        db.Index('idx_adjustment_serial', 'serial_no'),  # 按流水号查询
    ) 