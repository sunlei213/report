from app import db

class ClientRelation(db.Model):
    """客户关系模型"""
    __tablename__ = 'client_relations'
    
    id = db.Column(db.Integer, primary_key=True)
    account = db.Column(db.String(50), nullable=False, unique=True)  # 账号
    fenchen = db.Column(db.Numeric(5, 2), nullable=False, default=1)  # 分成比例 