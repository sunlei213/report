from app import db
from datetime import datetime

class Transaction(db.Model):
    """交易记录模型"""
    __tablename__ = 'transactions'
    
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    account = db.Column(db.String(50), nullable=False)  # 账号
    manager_id = db.Column(db.Integer, db.ForeignKey('managers.id'), nullable=False)
    
    # 产品信息直接记录,不强制关联products表
    product_code = db.Column(db.String(50), nullable=False)  # 产品代码
    product_name = db.Column(db.String(100), nullable=False)  # 产品名称
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=True)  # 可选关联到产品表
    
    amount = db.Column(db.Numeric(18, 2), nullable=False)  # 金额
    serial_no = db.Column(db.String(50), unique=True)  # 流水号,用于更新数据
    
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)  # 创建时间
    updated_at = db.Column(db.DateTime, onupdate=datetime.now)  # 更新时间
    
    # 关联
    manager = db.relationship('Manager')
    product = db.relationship('Product')  # 可选关联
    
    # 索引
    __table_args__ = (
        db.Index('idx_date_account', 'date', 'account'),  # 用于按日期和账号查询
        db.Index('idx_product_code', 'product_code'),     # 用于按产品代码查询
        db.Index('idx_serial_no', 'serial_no'),          # 用于按流水号查询
    ) 