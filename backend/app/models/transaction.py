from app import db

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
    
    amount = db.Column(db.Numeric(18, 2), nullable=False)  # 金额
    serial_no = db.Column(db.String(50), unique=True)  # 流水号,用于更新数据

    # 索引
    __table_args__ = (
        db.Index('idx_serial_no', 'serial_no'),          # 用于按流水号查询
    ) 