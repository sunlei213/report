from app import db
from datetime import datetime

class FixedIncome(db.Model):
    """固收产品模型"""
    __tablename__ = 'fixed_income'
    
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    no = db.Column(db.String(50), nullable=False)  # 申请编号
    account = db.Column(db.String(50), nullable=False)
    manager_id = db.Column(db.Integer, db.ForeignKey('managers.id'), nullable=False)
    amount = db.Column(db.Numeric(18, 2), nullable=False)
    serial_no = db.Column(db.String(50), unique=True)  # 流水号
    
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime, onupdate=datetime.now)
    
    # 关联
    manager = db.relationship('Manager', back_populates='fixed_income')
    
    # 索引
    __table_args__ = (
        db.Index('idx_fixed_date', 'date'),
        db.Index('idx_fixed_account', 'account'),
        db.Index('idx_fixed_serial', 'serial_no'),
    ) 