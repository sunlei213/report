"""add fixed and private tables

Revision ID: 2a3b4c5d6e7f
Revises: 1a2b3c4d5e6f
Create Date: 2024-01-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '2a3b4c5d6e7f'
down_revision = '1a2b3c4d5e6f'
branch_labels = None
depends_on = None

def upgrade():
    # 创建固收表
    op.create_table('fixed_income',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('date', sa.Date(), nullable=False),
        sa.Column('no', sa.String(length=50), nullable=False),  # 申请编号
        sa.Column('account', sa.String(length=50), nullable=False),
        sa.Column('manager_id', sa.Integer(), nullable=False),
        sa.Column('amount', sa.Numeric(precision=18, scale=2), nullable=False),
        sa.Column('serial_no', sa.String(length=50), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['manager_id'], ['managers.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('serial_no')
    )

    # 创建私募表
    op.create_table('private_fund',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('date', sa.Date(), nullable=False),
        sa.Column('account', sa.String(length=50), nullable=False),
        sa.Column('manager_id', sa.Integer(), nullable=False),
        sa.Column('product_code', sa.String(length=50), nullable=False),
        sa.Column('product_name', sa.String(length=100), nullable=False),
        sa.Column('product_id', sa.Integer(), nullable=True),
        sa.Column('amount', sa.Numeric(precision=18, scale=2), nullable=False),
        sa.Column('serial_no', sa.String(length=50), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['manager_id'], ['managers.id'], ),
        sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('serial_no')
    )

    # 创建索引
    op.create_index('idx_fixed_date', 'fixed_income', ['date'])
    op.create_index('idx_fixed_account', 'fixed_income', ['account'])
    op.create_index('idx_fixed_serial', 'fixed_income', ['serial_no'])
    
    op.create_index('idx_private_date', 'private_fund', ['date'])
    op.create_index('idx_private_account', 'private_fund', ['account'])
    op.create_index('idx_private_product', 'private_fund', ['product_code'])
    op.create_index('idx_private_serial', 'private_fund', ['serial_no'])

def downgrade():
    # 删除表
    op.drop_table('private_fund')
    op.drop_table('fixed_income') 