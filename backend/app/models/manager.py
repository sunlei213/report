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
    adjustments = db.relationship('Adjustment', back_populates='manager')
    fixed_income = db.relationship('FixedIncome', back_populates='manager')
    private_fund = db.relationship('PrivateFund', back_populates='manager')
    client_relations = db.relationship('ClientRelation', back_populates='manager')

class ManagerGroup(db.Model):
    """客户经理组别模型"""
    __tablename__ = 'manager_groups'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    order = db.Column(db.Integer, default=0)  # 排序字段
    
    # 关联
    managers = db.relationship('Manager', back_populates='group') 