from app import create_app, db
from sqlalchemy import text

app = create_app()

def migrate():
    """添加流水号字段的迁移脚本"""
    with app.app_context():
        # 为transactions表添加serial_no字段
        db.session.execute(text("""
            ALTER TABLE transactions 
            ADD COLUMN serial_no VARCHAR(50) UNIQUE,
            ADD COLUMN created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            ADD COLUMN updated_at DATETIME;
            
            CREATE INDEX idx_serial_no ON transactions (serial_no);
        """))
        
        # 为adjustments表添加serial_no字段
        db.session.execute(text("""
            ALTER TABLE adjustments 
            ADD COLUMN serial_no VARCHAR(50) UNIQUE,
            ADD COLUMN created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            ADD COLUMN updated_at DATETIME;
            
            CREATE INDEX idx_adjustment_serial ON adjustments (serial_no);
        """))
        
        # 为client_relations表添加serial_no字段
        db.session.execute(text("""
            ALTER TABLE client_relations 
            ADD COLUMN serial_no VARCHAR(50) UNIQUE,
            ADD COLUMN created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            ADD COLUMN updated_at DATETIME;
            
            CREATE INDEX idx_client_relation_serial ON client_relations (serial_no);
            
            -- 移除旧的唯一约束
            DROP INDEX IF EXISTS account ON client_relations;
            -- 添加新的唯一约束
            CREATE UNIQUE INDEX uk_account ON client_relations (account);
        """))
        
        db.session.commit()

if __name__ == '__main__':
    migrate() 