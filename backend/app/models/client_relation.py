from app import db
from datetime import datetime

class ClientRelation(db.Model):
    """客户关系模型"""
    __tablename__ = 'client_relations'
    
    id = db.Column(db.Integer, primary_key=True)
    account = db.Column(db.String(50), nullable=False)  # 账号
    manager_id = db.Column(db.Integer, db.ForeignKey('managers.id'), nullable=False)  # 客户经理
    fenchen = db.Column(db.Numeric(5, 2), nullable=False, default=1)  # 分成比例
    
    # 关联
    manager = db.relationship('Manager', back_populates='client_relations')
    
    # 索引
    __table_args__ = (
        db.Index('idx_account', 'account'),  # 按账号查询
    ) 