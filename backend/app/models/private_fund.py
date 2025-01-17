from app import db
from datetime import datetime

class PrivateFund(db.Model):
    """私募产品模型"""
    __tablename__ = 'private_fund'
    
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    account = db.Column(db.String(50), nullable=False)
    manager_id = db.Column(db.Integer, db.ForeignKey('managers.id'), nullable=False)
    product_code = db.Column(db.String(50), nullable=False)
    product_name = db.Column(db.String(100), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=True)
    amount = db.Column(db.Numeric(18, 2), nullable=False)
    serial_no = db.Column(db.String(50), unique=True)  # 流水号
    
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime, onupdate=datetime.now)
    
    # 关联
    manager = db.relationship('Manager', back_populates='private_fund')
    product = db.relationship('Product', back_populates='private_fund')
    
    # 索引
    __table_args__ = (
        db.Index('idx_private_date', 'date'),
        db.Index('idx_private_account', 'account'),
        db.Index('idx_private_product', 'product_code'),
        db.Index('idx_private_serial', 'serial_no'),
    ) 