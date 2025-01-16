from app import db

class ManagerGroup(db.Model):
    """客户经理组别模型"""
    __tablename__ = 'manager_groups'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    order = db.Column(db.Integer, default=0)  # 排序字段
    
    # 关联
    managers = db.relationship('Manager', back_populates='group') 