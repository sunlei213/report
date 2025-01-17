from app import db
from datetime import datetime

class ClientRelation(db.Model):
    """客户关系模型"""
    __tablename__ = 'client_relations'
    
    id = db.Column(db.Integer, primary_key=True)
    account = db.Column(db.String(50), nullable=False)  # 账号
    manager_id = db.Column(db.Integer, db.ForeignKey('managers.id'), nullable=False)  # 客户经理
    fenchen = db.Column(db.Numeric(5, 2), nullable=False, default=1)  # 分成比例
    serial_no = db.Column(db.String(50), unique=True)  # 流水号,用于更新数据
    
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)  # 创建时间
    updated_at = db.Column(db.DateTime, onupdate=datetime.now)  # 更新时间
    
    # 关联
    manager = db.relationship('Manager', back_populates='client_relations')
    
    # 索引
    __table_args__ = (
        db.Index('idx_account', 'account'),  # 按账号查询
        db.Index('idx_serial_no', 'serial_no'),  # 按流水号查询
        db.UniqueConstraint('account', name='uk_account')  # 账号唯一约束
    ) 