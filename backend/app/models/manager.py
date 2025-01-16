from app import db

class Manager(db.Model):
    """客户经理模型"""
    __tablename__ = 'managers'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('manager_groups.id'), nullable=False)
    order = db.Column(db.Integer, default=0)  # 排序字段
    
    # 关联
    group = db.relationship('ManagerGroup', back_populates='managers')
    targets = db.relationship('GroupTarget', back_populates='manager')
    transactions = db.relationship('Transaction', back_populates='manager')
    adjustments = db.relationship('Adjustment', back_populates='manager')  # 添加调整数据关联 